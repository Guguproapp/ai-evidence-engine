import struct
import zlib


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_rgb_png(path, width, height, pixels):
    if len(pixels) != width * height * 3:
        raise ValueError("RGB pixel buffer size does not match dimensions")
    rows = bytearray()
    stride = width * 3
    for y in range(height):
        rows.append(0)
        rows.extend(pixels[y * stride:(y + 1) * stride])
    data = PNG_SIGNATURE
    data += _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    data += _chunk(b"IDAT", zlib.compress(bytes(rows), 9))
    data += _chunk(b"IEND", b"")
    with open(path, "wb") as file:
        file.write(data)


def solid_canvas(width, height, color):
    return bytearray(color * (width * height))


def set_pixel(pixels, width, height, x, y, color):
    if 0 <= x < width and 0 <= y < height:
        offset = (y * width + x) * 3
        pixels[offset:offset + 3] = bytes(color)


def fill_rect(pixels, width, height, x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(height, y1)):
        for x in range(max(0, x0), min(width, x1)):
            set_pixel(pixels, width, height, x, y, color)


def fill_ellipse(pixels, width, height, cx, cy, rx, ry, color):
    for y in range(max(0, cy - ry), min(height, cy + ry + 1)):
        for x in range(max(0, cx - rx), min(width, cx + rx + 1)):
            if ((x - cx) ** 2) / max(1, rx ** 2) + ((y - cy) ** 2) / max(1, ry ** 2) <= 1:
                set_pixel(pixels, width, height, x, y, color)


FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01110"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    " ": ("00000",) * 7,
}


def draw_text(pixels, width, height, x, y, text, color, scale=4):
    cursor = x
    for character in text.upper():
        glyph = FONT.get(character, FONT[" "])
        for gy, row in enumerate(glyph):
            for gx, value in enumerate(row):
                if value == "1":
                    fill_rect(pixels, width, height, cursor + gx * scale, y + gy * scale, cursor + (gx + 1) * scale, y + (gy + 1) * scale, color)
        cursor += 6 * scale


def diff_mask(before, after, width, height, threshold=12):
    if len(before) != len(after) or len(before) != width * height * 3:
        raise ValueError("Image buffers must have equal RGB dimensions")
    mask = bytearray(width * height * 3)
    changed = []
    for index in range(width * height):
        offset = index * 3
        delta = max(abs(before[offset + channel] - after[offset + channel]) for channel in range(3))
        if delta >= threshold:
            mask[offset:offset + 3] = b"\xff\xff\xff"
            changed.append((index % width, index // width))
    if not changed:
        bbox = None
    else:
        xs = [point[0] for point in changed]
        ys = [point[1] for point in changed]
        bbox = {"x": min(xs), "y": min(ys), "width": max(xs) - min(xs) + 1, "height": max(ys) - min(ys) + 1}
    ratio = round(len(changed) / (width * height), 6)
    return mask, {
        "changed_pixels": len(changed),
        "total_pixels": width * height,
        "spatial_change_ratio": ratio,
        "changed_region": bbox,
        "pixel_threshold": threshold,
        # Legacy aliases remain until existing demo consumers migrate.
        "changed_ratio": ratio,
        "bounding_box": bbox,
        "threshold": threshold,
    }


def comparison_image(before, after, mask, width, height):
    output = bytearray(width * height * 3)
    for index in range(width * height):
        offset = index * 3
        if mask[offset] == 255:
            output[offset:offset + 3] = bytes((242, 79, 66))
        else:
            output[offset:offset + 3] = bytes(((before[offset] + after[offset]) // 2, (before[offset + 1] + after[offset + 1]) // 2, (before[offset + 2] + after[offset + 2]) // 2))
    return output
