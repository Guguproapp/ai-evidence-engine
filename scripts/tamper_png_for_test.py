import struct
import sys
import zlib
from pathlib import Path


def tamper(source, output):
    data = Path(source).read_bytes()
    result = bytearray(data[:8])
    offset = 8
    changed = False
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        offset += length + 12
        if kind == b"IDAT" and not changed:
            raw = bytearray(zlib.decompress(payload))
            raw[1000] ^= 0x20
            payload = zlib.compress(bytes(raw), 9)
            changed = True
        result += struct.pack(">I", len(payload))
        result += kind + payload
        result += struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    if not changed:
        raise RuntimeError("PNG did not contain an IDAT chunk")
    Path(output).write_bytes(result)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: tamper_png_for_test.py SOURCE OUTPUT")
    tamper(sys.argv[1], sys.argv[2])
