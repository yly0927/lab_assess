# okti_encoder.py
from PIL import Image

def encode_okti(image_path, okti_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    pixels = list(img.getdata())

    lines = ["okti", f"{width} {height}"]

    current_color = None
    repeat_count = 0

    def format_color(c):
        return f"{c[0]:02X}{c[1]:02X}{c[2]:02X}"

    for pixel in pixels:
        if pixel == current_color:
            repeat_count += 1
        else:
            if current_color is not None:
                if repeat_count == 1:
                    lines.append(f"p{format_color(current_color)}")
                else:
                    lines.append(f"n{repeat_count:X}")
                    lines.append(f"p{format_color(current_color)}")
            
            current_color = pixel
            repeat_count = 1

    if current_color is not None:
        if repeat_count == 1:
            lines.append(f"p{format_color(current_color)}")
        else:
            lines.append(f"n{repeat_count:X}")
            lines.append(f"p{format_color(current_color)}")

    with open(okti_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))