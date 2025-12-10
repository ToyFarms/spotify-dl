# pyright: basic
import argparse
import os
import subprocess
from pathlib import Path
import sys
from typing import Protocol, override


class SupportsStr(Protocol):
    def __str__(self) -> str: ...


def call(_cmd: list[SupportsStr]) -> None:
    cmd = list(map(str, _cmd))

    print(f"* {cmd}")
    ret = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    print(f"finished with code {ret.returncode}")


def main() -> None:
    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("build-bento4")

    args = parser.parse_args()
    if args.cmd == "build-bento4":
        print("===== PREREQUISITES =====")
        print("cmake, make, c++ compiler, c++ runtime")

        bento = Path("bento4")
        if not bento.exists():
            print(
                "bento4/ directory does not exists, clone submodule with `git submodule update --init --recursive or download the source yourself"
            )
            return

        if bento.is_file():
            print("bento4 is not a directory")
            return

        build = Path("build")
        build.mkdir(exist_ok=True)

        os.chdir(build)
        call(["cmake", ".." / bento])
        call(["make", "-j", (os.cpu_count() or 4) // 2])


if __name__ == "__main__":
    main()
