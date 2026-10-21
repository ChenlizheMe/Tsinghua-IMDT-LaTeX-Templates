"""Add Unicode access to the legacy Word Symbol root glyph, for private use.

The input remains unchanged. All outlines, metrics and hinting are copied intact.
Only cmap and the required sfnt checksum adjustment differ. No dependency needed.
"""
import argparse
from pathlib import Path
import struct


def checksum(data):
    data += b'\0' * (-len(data) % 4)
    return sum(struct.unpack('>' + 'I' * (len(data) // 4), data)) & 0xFFFFFFFF


def prepare(source, destination):
    original = source.read_bytes()
    assert original[:4] == b'\0\1\0\0', 'Expected a TrueType Symbol font'
    count = struct.unpack_from('>H', original, 4)[0]
    tables = {}
    for i in range(count):
        tag, _, offset, length = struct.unpack_from('>4sIII', original, 12 + 16 * i)
        tables[tag] = original[offset:offset + length]
    cmap = tables[b'cmap']
    subtables = []
    root_gid = None
    space_gid = None
    for i in range(struct.unpack_from('>H', cmap, 2)[0]):
        platform, encoding, offset = struct.unpack_from('>HHI', cmap, 4 + i * 8)
        fmt, length = struct.unpack_from('>HH', cmap, offset)
        assert fmt in (0, 4, 6), 'Unexpected cmap format in legacy Symbol font'
        sub = cmap[offset:offset + length]
        subtables.append((platform, encoding, sub))
        if (platform, encoding, fmt) != (3, 0, 4):
            continue
        n = struct.unpack_from('>H', sub, 6)[0] // 2
        end, start, delta, ranges = 14, 16 + 2*n, 16 + 4*n, 16 + 6*n
        def gid(code):
            u16 = lambda p: struct.unpack_from('>H', sub, p)[0]
            for j in range(n):
                if u16(start + 2*j) <= code <= u16(end + 2*j):
                    ro = u16(ranges + 2*j)
                    if not ro:
                        return (code + u16(delta + 2*j)) & 0xFFFF
                    g = u16(ranges + 2*j + ro + 2*(code-u16(start+2*j)))
                    return (g + u16(delta+2*j)) & 0xFFFF if g else 0
            return 0
        root_gid, space_gid = gid(0xF0D6), gid(0xF020)
    assert root_gid and space_gid, 'Symbol private-use root/space glyphs missing'
    codes = (0x20, 0x221A, 0xFFFF)
    gids = (space_gid, root_gid, 0)
    words = (4, 40, 0, 6, 4, 1, 2, *codes, 0, *codes,
             *((g-c) & 0xFFFF for c, g in zip(codes, gids)), 0, 0, 0)
    unicode_sub = struct.pack('>' + 'H'*len(words), *words)
    assert len(unicode_sub) == 40
    subtables = [s for s in subtables if s[:2] not in ((0, 3), (3, 1))]
    subtables.extend(((0, 3, unicode_sub), (3, 1, unicode_sub)))
    subtables.sort(key=lambda s: s[:2])
    directory = bytearray(struct.pack('>HH', 0, len(subtables)))
    payload = bytearray()
    for platform, encoding, sub in subtables:
        directory += struct.pack('>HHI', platform, encoding, 4+8*len(subtables)+len(payload))
        payload += sub
    tables[b'cmap'] = bytes(directory + payload)
    head = bytearray(tables[b'head']); head[8:12] = b'\0'*4
    tables[b'head'] = bytes(head)
    directory = bytearray(original[:12]); payload = bytearray()
    head_offset = None
    for tag, data in sorted(tables.items()):
        offset = 12 + 16*count + len(payload)
        if tag == b'head':
            head_offset = offset
        directory += struct.pack('>4sIII', tag, checksum(data), offset, len(data))
        payload += data + b'\0' * (-len(data) % 4)
    output = directory + payload
    struct.pack_into('>I', output, head_offset+8, (0xB1B0AFBA-checksum(output)) & 0xFFFFFFFF)
    assert checksum(output) == 0xB1B0AFBA
    assert source.resolve() != destination.resolve(), 'Keep the original font unchanged'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(output)
    print(f'Prepared {destination.name}: original glyph {root_gid}, Unicode U+221A; outlines unchanged.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Your Windows symbol.ttf')
    parser.add_argument('destination', type=Path, help='Private fonts/symbol-unicode.ttf')
    args = parser.parse_args()
    prepare(args.source, args.destination)
