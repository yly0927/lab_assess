# okti_encoder.py
from PIL import Image


def encode_okti(image_path, okti_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    px = img.load()
    pixels = [px[x, y] for y in range(height) for x in range(width)]

    lines = ["okti", f"{width} {height}"]

    current_color = None
    repeat_count = 0

    def format_color(c):
        return f"{c[0]:02X}{c[1]:02X}{c[2]:02X}"

    def flush_run():
        if current_color is None:
            return
        if repeat_count == 1:
            lines.append(f"p{format_color(current_color)}")
        else:
            lines.append(f"n{repeat_count:X}")
            lines.append(f"p{format_color(current_color)}")

    for pixel in pixels:
        if pixel == current_color:
            repeat_count += 1
        else:
            flush_run()
            current_color = pixel
            repeat_count = 1

    flush_run()

    with open(okti_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
