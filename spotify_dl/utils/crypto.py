import os
import struct

from .bytes_stuff import to_bytes


class DHKey:
    PRIME: int = (
        1552518092300708935130918131258481755631334049434514313202351194902966239949102107258669453876591642442910007680288864229150803718918046342632727613031282983744380820890196288509170691316593175367469551763119843371637221007210577919
    )

    def __init__(self) -> None:
        self.private: int = int.from_bytes(os.urandom(0x5F), "big")
        self.public: int = pow(2, self.private, self.PRIME)

        self.private_bytes: bytes = to_bytes(self.private)
        self.public_bytes: bytes = to_bytes(self.public)

    def shared_key(self, remote_key: bytes) -> bytes:
        return to_bytes(pow(int.from_bytes(remote_key), self.private, self.PRIME))


class Shannon:
    n: int = 16
    fold: int = n
    initkonst: int = 0x6996C53A
    keyp: int = 13
    r: list[int]
    crc: list[int]
    init_r: list[int]
    konst: int = initkonst
    sbuf: int = 0
    mbuf: int = 0
    nbuf: int = 0

    def __init__(self):
        self.r = [0 for _ in range(self.n)]
        self.crc = [0 for _ in range(self.n)]
        self.init_r = [0 for _ in range(self.n)]

    def rotl(self, i: int, distance: int) -> int:
        return ((i << distance) | (i >> (32 - distance))) & 0xFFFFFFFF

    def sbox(self, i: int) -> int:
        i ^= self.rotl(i, 5) | self.rotl(i, 7)
        i ^= self.rotl(i, 19) | self.rotl(i, 22)
        return i

    def sbox2(self, i: int) -> int:
        i ^= self.rotl(i, 7) | self.rotl(i, 22)
        i ^= self.rotl(i, 5) | self.rotl(i, 19)
        return i

    def cycle(self) -> None:
        t: int
        t = self.r[12] ^ self.r[13] ^ self.konst
        t = self.sbox(t) ^ self.rotl(self.r[0], 1)
        for i in range(1, self.n):
            self.r[i - 1] = self.r[i]
        self.r[self.n - 1] = t
        t = self.sbox2(self.r[2] ^ self.r[15])
        self.r[0] ^= t
        self.sbuf = t ^ self.r[8] ^ self.r[12]

    def crc_func(self, i: int) -> None:
        t: int
        t = self.crc[0] ^ self.crc[2] ^ self.crc[15] ^ i
        for j in range(1, self.n):
            self.crc[j - 1] = self.crc[j]
        self.crc[self.n - 1] = t

    def mac_func(self, i: int) -> None:
        self.crc_func(i)
        self.r[self.keyp] ^= i

    def init_state(self) -> None:
        self.r[0] = 1
        self.r[1] = 1
        for i in range(2, self.n):
            self.r[i] = self.r[i - 1] + self.r[i - 2]
        self.konst = self.initkonst

    def save_state(self) -> None:
        for i in range(self.n):
            self.init_r[i] = self.r[i]

    def reload_state(self) -> None:
        for i in range(self.n):
            self.r[i] = self.init_r[i]

    def gen_konst(self) -> None:
        self.konst = self.r[0]

    def add_key(self, k: int) -> None:
        self.r[self.keyp] ^= k

    def diffuse(self) -> None:
        for _ in range(self.fold):
            self.cycle()

    def load_key(self, key: bytes) -> None:
        i: int
        _: int
        _: int
        padding_size = int((len(key) + 3) / 4) * 4 - len(key)
        key = key + (b"\x00" * padding_size) + struct.pack("<I", len(key))
        for i in range(0, len(key), 4):
            self.r[self.keyp] = (
                self.r[self.keyp] ^ struct.unpack("<I", key[i : i + 4])[0]
            )
            self.cycle()
        for i in range(self.n):
            self.crc[i] = self.r[i]
        self.diffuse()
        for i in range(self.n):
            self.r[i] ^= self.crc[i]

    def key(self, key: bytes) -> None:
        self.init_state()
        self.load_key(key)
        self.gen_konst()
        self.save_state()
        self.nbuf = 0

    def nonce(self, _nonce: bytes | int) -> None:
        nonce = (
            _nonce if isinstance(_nonce, bytes) else bytes(struct.pack(">I", _nonce))
        )
        self.reload_state()
        self.konst = self.initkonst
        self.load_key(nonce)
        self.gen_konst()
        self.nbuf = 0

    def encrypt(self, _buffer: bytes, n: int | None = None) -> bytes:
        if n is None:
            return self.encrypt(_buffer, len(_buffer))
        buffer = bytearray(_buffer)
        i = 0
        j: int
        t: int
        if self.nbuf != 0:
            while self.nbuf != 0 and n != 0:
                self.mbuf ^= (buffer[i] & 0xFF) << (32 - self.nbuf)
                buffer[i] ^= (self.sbuf >> (32 - self.nbuf)) & 0xFF
                i += 1
                self.nbuf -= 8
                n -= 1
            if self.nbuf != 0:
                return b""
            self.mac_func(self.mbuf)
        j = n & ~0x03
        while i < j:
            self.cycle()
            t = (
                ((buffer[i + 3] & 0xFF) << 24)
                | ((buffer[i + 2] & 0xFF) << 16)
                | ((buffer[i + 1] & 0xFF) << 8)
                | (buffer[i] & 0xFF)
            )
            self.mac_func(t)
            t ^= self.sbuf
            buffer[i + 3] = (t >> 24) & 0xFF
            buffer[i + 2] = (t >> 16) & 0xFF
            buffer[i + 1] = (t >> 8) & 0xFF
            buffer[i] = t & 0xFF
            i += 4
        n &= 0x03
        if n != 0:
            self.cycle()
            self.mbuf = 0
            self.nbuf = 32
            while self.nbuf != 0 and n != 0:
                self.mbuf ^= (buffer[i] & 0xFF) << (32 - self.nbuf)
                buffer[i] ^= (self.sbuf >> (32 - self.nbuf)) & 0xFF
                i += 1
                self.nbuf -= 8
                n -= 1
        return bytes(buffer)

    def decrypt(self, _buffer: bytes, n: int | None = None) -> bytes:
        if n is None:
            return self.decrypt(_buffer, len(_buffer))
        buffer = bytearray(_buffer)
        i = 0
        j: int
        t: int
        if self.nbuf != 0:
            while self.nbuf != 0 and n != 0:
                buffer[i] ^= (self.sbuf >> (32 - self.nbuf)) & 0xFF
                self.mbuf ^= (buffer[i] & 0xFF) << (32 - self.nbuf)
                i += 1
                self.nbuf -= 8
                n -= 1
            if self.nbuf != 0:
                return b""
            self.mac_func(self.mbuf)
        j = n & ~0x03
        while i < j:
            self.cycle()
            t = (
                ((buffer[i + 3] & 0xFF) << 24)
                | ((buffer[i + 2] & 0xFF) << 16)
                | ((buffer[i + 1] & 0xFF) << 8)
                | (buffer[i] & 0xFF)
            )
            t ^= self.sbuf
            self.mac_func(t)
            buffer[i + 3] = (t >> 24) & 0xFF
            buffer[i + 2] = (t >> 16) & 0xFF
            buffer[i + 1] = (t >> 8) & 0xFF
            buffer[i] = t & 0xFF
            i += 4
        n &= 0x03
        if n != 0:
            self.cycle()
            self.mbuf = 0
            self.nbuf = 32
            while self.nbuf != 0 and n != 0:
                buffer[i] ^= (self.sbuf >> (32 - self.nbuf)) & 0xFF
                self.mbuf ^= (buffer[i] & 0xFF) << (32 - self.nbuf)
                i += 1
                self.nbuf -= 8
                n -= 1
        return bytes(buffer)

    def finish(self, n: int) -> bytes:
        buffer = bytearray(4)
        i = 0
        j: int
        if self.nbuf != 0:
            self.mac_func(self.mbuf)
        self.cycle()
        self.add_key(self.initkonst ^ (self.nbuf << 3))
        self.nbuf = 0
        for j in range(self.n):
            self.r[j] ^= self.crc[j]
        self.diffuse()
        while n > 0:
            self.cycle()
            if n >= 4:
                buffer[i + 3] = (self.sbuf >> 24) & 0xFF
                buffer[i + 2] = (self.sbuf >> 16) & 0xFF
                buffer[i + 1] = (self.sbuf >> 8) & 0xFF
                buffer[i] = self.sbuf & 0xFF
                n -= 4
                i += 4
            else:
                for j in range(n):
                    buffer[i + j] = (self.sbuf >> (i * 8)) & 0xFF
                break
        return bytes(buffer)
