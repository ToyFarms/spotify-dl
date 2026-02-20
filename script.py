# pyright: basic
import argparse
import os
import platform
import shutil
import subprocess
from pathlib import Path
import sys
from typing import Literal, Protocol, Sequence
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import constant_time
import secrets


class SupportsStr(Protocol):
    def __str__(self) -> str: ...


def call(_cmd: Sequence[SupportsStr]) -> None:
    cmd = list(map(str, _cmd))

    print(f"* {cmd}")
    ret = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    print(f"finished with code {ret.returncode}")


_MAGIC = b"SPDv1"
_SALT_SIZE = 16
_NONCE_SIZE = 12
_KEY_LEN = 32
_PBKDF2_ITERS = 400_000


def derive_key(password: bytes, salt: bytes, iterations: int = _PBKDF2_ITERS) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=_KEY_LEN,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password)


def encrypt_file(
    input_path: Path,
    output_path: Path,
    password: bytes,
    force: bool = False,
) -> None:
    if output_path.exists() and not force:
        print(f"file {output_path} exists. use --force to overwrite.")
        sys.exit(2)

    with input_path.open("rb") as f:
        plaintext = f.read()

    salt = secrets.token_bytes(_SALT_SIZE)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(_NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

    with output_path.open("wb") as f:
        f.write(_MAGIC)
        f.write(salt)
        f.write(nonce)
        f.write(ciphertext)

    print(f"encrypted {input_path} -> {output_path}")


def decrypt_file(
    input_path: Path,
    output_path: Path,
    password: bytes,
    force: bool = False,
) -> None:
    if output_path.exists() and not force:
        print(f"file {output_path} exists. use --force to overwrite.")
        sys.exit(2)

    with input_path.open("rb") as f:
        data = f.read()

    min_len = len(_MAGIC) + _SALT_SIZE + _NONCE_SIZE + 16
    if len(data) < min_len:
        print("input file too small or corrupt.")
        sys.exit(3)

    offset = 0
    magic = data[offset : offset + len(_MAGIC)]
    offset += len(_MAGIC)
    if not constant_time.bytes_eq(magic, _MAGIC):
        print("bad file format or unsupported version.")
        sys.exit(4)

    salt = data[offset : offset + _SALT_SIZE]
    offset += _SALT_SIZE
    nonce = data[offset : offset + _NONCE_SIZE]
    offset += _NONCE_SIZE
    ciphertext = data[offset:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    except Exception as e:
        print(
            "decryption failed: authentication error (wrong password or corrupted file)."
        )
        sys.exit(5)

    with output_path.open("wb") as f:
        f.write(plaintext)

    print(f"decrypted {input_path} -> {output_path}")


def read_password() -> bytes:
    try:
        pw = getpass.getpass("password: ")
        if pw:
            return pw.encode("utf-8")
    except (EOFError, KeyboardInterrupt):
        pass

    line = sys.stdin.buffer.readline()
    if not line:
        print("no password provided on stdin.")
        sys.exit(6)
    return line.rstrip(b"\n\r")


def default_output_path(input_path: Path, mode: Literal["enc", "dec"] | str) -> Path:
    name = input_path.name

    if mode == "enc":
        return input_path.with_name(name + ".enc")
    if mode == "dec":
        if name.endswith(".enc"):
            return input_path.with_name(name[:-4])

        suffixes = input_path.suffixes
        base = input_path.name
        for s in suffixes:
            base = base[: -len(s)]

        new_name = base + ".dec" + "".join(suffixes)
        return input_path.with_name(new_name)

    raise ValueError("mode must be 'enc' or 'dec'")


def detect_mingw_prefix():
    prefixes = ["x86_64-w64-mingw32", "i686-w64-mingw32"]
    for p in prefixes:
        if shutil.which(f"{p}-g++"):
            return p

    if shutil.which("g++") and (
        "MINGW" in platform.system().upper() or shutil.which("mingw32-make")
    ):
        return None
    return None


def detect_msvc():
    return shutil.which("cl") is not None


def choose_make_command():
    if shutil.which("mingw32-make"):
        return ["mingw32-make"]
    if shutil.which("make"):
        return ["make"]

    return None


def build_bento4():
    print("===== PREREQUISITES =====")
    print("cmake, make (or mingw32-make), c++ compiler, c++ runtime")

    project_root = Path.cwd()
    bento = project_root / "bento4"
    if not bento.exists():
        print(
            "bento4/ directory does not exists, clone submodule with `git submodule update --init --recursive` or download the source yourself"
        )
        return

    if bento.is_file():
        print("bento4 is not a directory")
        return

    host = platform.system()
    print(f"host platform: {host}")

    mingw_prefix = detect_mingw_prefix()
    mingw_native = False
    if host == "Windows":
        if shutil.which("mingw32-make") or shutil.which("g++"):
            mingw_native = True
            print("detected native MinGW toolchain on Windows.")
    else:
        if mingw_prefix:
            print(
                f"detected MinGW cross-compiler prefix: {mingw_prefix} (will cross-compile to Windows)"
            )
        else:
            print("no MinGW cross-compiler detected.")

    msvc_present = detect_msvc() and host == "Windows"
    if msvc_present:
        print("detected MSVC (cl.exe) on Windows.")

    native_gcc = shutil.which("gcc") or shutil.which("g++")
    if native_gcc:
        print(f"detected native host GCC at: {native_gcc}")

    base_cmake_args = [
        "-DCMAKE_BUILD_TYPE=Release",
        "-DBUILD_SHARED_LIBRARY=OFF",
        "-DBUILD_APPS=ON",
    ]

    build_tasks = []

    if host != "Windows" and native_gcc and mingw_prefix:
        build_tasks.append({"name": "linux", "type": "native"})
        build_tasks.append({"name": "windows", "type": "mingw-cross"})
        print("Configured to build both: native Linux and MinGW Windows cross-build.")
    else:
        if host == "Windows":
            if msvc_present:
                build_tasks.append({"name": "windows", "type": "msvc"})
            elif mingw_native:
                build_tasks.append({"name": "windows", "type": "mingw-native"})
            else:
                build_tasks.append({"name": "windows", "type": "generic"})
        else:
            if native_gcc:
                build_tasks.append({"name": "linux", "type": "native"})
            else:
                print("No suitable native compiler found; aborting.")
                return

    def run_task(task):
        name = task["name"]
        ttype = task["type"]
        build_root = project_root / "build" / f"{name}-release"
        build_root.mkdir(parents=True, exist_ok=True)

        cmake_args = list(base_cmake_args)
        toolchain_file = None

        if ttype in ("native", "mingw-cross", "mingw-native"):
            project_abs = str(project_root.resolve())
            common_flags = (
                f"-g0 -s "
                f"-ffile-prefix-map={project_abs}=. "
                f"-fmacro-prefix-map={project_abs}=. "
                f"-fdebug-prefix-map={project_abs}=. "
                f"-fno-ident"
            )

            cmake_args += [
                f"-DCMAKE_C_FLAGS_RELEASE={common_flags}",
                f"-DCMAKE_CXX_FLAGS_RELEASE={common_flags}",
                f"-DCMAKE_EXE_LINKER_FLAGS_RELEASE=-s -static-libgcc -static-libstdc++",
                "-DCMAKE_STRIP=strip",
            ]
        elif ttype == "msvc":
            cmake_args += [
                "-DCMAKE_C_FLAGS_RELEASE=/Brepro /O2",
                "-DCMAKE_CXX_FLAGS_RELEASE=/Brepro /O2",
                "-DCMAKE_EXE_LINKER_FLAGS_RELEASE=/DEBUG:NONE",
            ]

        if ttype == "native" and name == "linux":
            cc = shutil.which("gcc") or ""
            cxx = shutil.which("g++") or ""
            if cc and cxx:
                cmake_args += [
                    f"-DCMAKE_C_COMPILER={cc}",
                    f"-DCMAKE_CXX_COMPILER={cxx}",
                ]
                print(f"[{name}] using host compilers: {cc}, {cxx}")
            else:
                print(
                    f"[{name}] host gcc/g++ not found; using system default compilers"
                )

        elif ttype == "mingw-cross" and mingw_prefix:
            toolchain_file = build_root / "mingw-toolchain.cmake"
            content = f"""set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_VERSION 1)

set(CMAKE_C_COMPILER   {mingw_prefix}-gcc)
set(CMAKE_CXX_COMPILER {mingw_prefix}-g++)
set(CMAKE_RC_COMPILER  {mingw_prefix}-windres)

# Do not search the host paths for programs
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
"""
            toolchain_file.write_text(content)
            print(f"[{name}] generated toolchain file: {toolchain_file}")
            cmake_args += [f"-DCMAKE_TOOLCHAIN_FILE={toolchain_file}"]

        elif ttype == "mingw-native" and host == "Windows":
            gcc_path = shutil.which("gcc") or ""
            gpp_path = shutil.which("g++") or ""
            if gcc_path or gpp_path:
                cmake_args += [
                    f"-DCMAKE_C_COMPILER={gcc_path}",
                    f"-DCMAKE_CXX_COMPILER={gpp_path}",
                ]
                print(f"[{name}] using native MinGW compilers: {gcc_path}, {gpp_path}")

        elif ttype == "msvc" and host == "Windows":
            print(f"[{name}] building with MSVC (cl.exe)")

        else:
            print(f"[{name}] generic build (no special compiler flags)")

        prev_cwd = os.getcwd()
        try:
            os.chdir(build_root)
            source_dir = str(bento.resolve())
            cmake_cmd = ["cmake", source_dir] + cmake_args
            print(f"[{name}] running CMake configure: {' '.join(cmake_cmd)}")
            call(cmake_cmd)

            make_cmd = choose_make_command()
            nprocs = max(1, (os.cpu_count() or 4) // 2)

            if host == "Windows" and ttype == "msvc":
                config = "Release"
                build_cmd = [
                    "cmake",
                    "--build",
                    ".",
                    "--config",
                    config,
                    "--",
                    f"-j{nprocs}",
                ]
                print(
                    f"[{name}] building with MSVC (cmake --build ...): {' '.join(build_cmd)}"
                )
                call(build_cmd)
            elif make_cmd:
                build_cmd = make_cmd + [f"-j{nprocs}"]
                print(f"[{name}] building with: {' '.join(build_cmd)}")
                call(build_cmd)
            else:
                build_cmd = ["cmake", "--build", ".", "--", f"-j{nprocs}"]
                print(
                    f"[{name}] no plain 'make' found, using cmake --build: {' '.join(build_cmd)}"
                )
                call(build_cmd)

            if ttype in ("native", "mingw-cross", "mingw-native"):
                if strip_bin := shutil.which("strip"):
                    print(f"[{name}] stripping binaries...")
                    for exe in build_root.rglob("*"):
                        if exe.is_file() and os.access(exe, os.X_OK):
                            call([strip_bin, "--strip-all", str(exe)])

            print(f"[{name}] build complete. binaries are in {build_root}")

        finally:
            os.chdir(prev_cwd)

    for t in build_tasks:
        run_task(t)

    print("all requested builds finished.")


def main() -> None:
    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("build-bento4")
    encp = sub.add_parser(
        "enc", help="encrypt a file with a password (AES-256-GCM, PBKDF2-HMAC-SHA256)."
    )
    encp.add_argument(
        "-i", "--in", dest="infile", required=True, help="input file to encrypt"
    )
    encp.add_argument(
        "-o",
        "--out",
        dest="outfile",
        required=False,
        help="output file path",
    )
    encp.add_argument(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        help="overwrite output if exists",
    )

    decp = sub.add_parser(
        "dec", help="decrypt a file previously encrypted by this tool"
    )
    decp.add_argument(
        "-i", "--in", dest="infile", required=True, help="input file to decrypt"
    )
    decp.add_argument(
        "-o",
        "--out",
        dest="outfile",
        required=False,
        help="output file path",
    )
    decp.add_argument(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        help="overwrite output if exists",
    )

    args = parser.parse_args()
    if args.cmd == "build-bento4":
        build_bento4()
        cp = shutil.which("cp") or shutil.which("copy")
        Path("binaries").mkdir(exist_ok=True)
        try:
            call([cp, "build/linux-release/mp4decrypt", "binaries"])
        except:
            pass
        try:
            call([cp, "build/windows-release/mp4decrypt.exe", "binaries"])
        except:
            pass
    elif args.cmd == "enc":
        infile = Path(args.infile)
        if not infile.exists():
            print(f"input file {infile} does not exist.")
            sys.exit(1)
        outfile = (
            Path(args.outfile) if args.outfile else default_output_path(infile, "enc")
        )
        password = read_password()
        encrypt_file(infile, outfile, password, force=bool(args.force))

    elif args.cmd == "dec":
        infile = Path(args.infile)
        if not infile.exists():
            print(f"input file {infile} does not exist.")
            sys.exit(1)
        outfile = (
            Path(args.outfile) if args.outfile else default_output_path(infile, "dec")
        )
        password = read_password()
        decrypt_file(infile, outfile, password, force=bool(args.force))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
