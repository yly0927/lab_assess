# okti_decoder.py
import re
from PIL import Image

HEX_COLOR = re.compile(r"^[0-9A-Fa-f]{6}$")
HEX_COUNT = re.compile(r"^[0-9A-Fa-f]+$")


def decode_okti(okti_path, output_path):
    with open(okti_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines or lines[0] != "okti":
        raise ValueError("文件头不是 okti")

    if len(lines) < 2:
        raise ValueError("宽高行无效")

    parts = lines[1].split()
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        raise ValueError("宽高行无效")

    w, h = int(parts[0]), int(parts[1])
    if w <= 0 or h <= 0:
        raise ValueError("宽高行无效")

    expected = w * h
    pixels = []
    pending_repeat = 1
    ptr = 2

    while ptr < len(lines):
        cmd = lines[ptr]
        ptr += 1
        kind = cmd[0]

        if kind == "p":
            num_str = cmd[1:]
            if not HEX_COLOR.fullmatch(num_str):
                raise ValueError(f"颜色格式错误，预期6位十六进制: {cmd}")

            color = (
                int(num_str[0:2], 16),
                int(num_str[2:4], 16),
                int(num_str[4:6], 16),
            )
            if pending_repeat > max(expected * 2, 1_000_000):
                raise ValueError(f"重复次数过大: n{pending_repeat:X}")
            pixels.extend([color] * pending_repeat)
            pending_repeat = 1

        elif kind == "n":
            num_str = cmd[1:]
            if not num_str:
                raise ValueError(f"缺少重复次数: {cmd}")
            if not HEX_COUNT.fullmatch(num_str):
                raise ValueError(f"缺少重复次数: {cmd}")
            pending_repeat = int(num_str, 16)
            if pending_repeat < 1:
                raise ValueError(f"重复次数必须为正: {cmd}")
            if pending_repeat > max(expected * 2, 1_000_000):
                raise ValueError(f"重复次数过大: {cmd}")

        else:
            raise ValueError(f"未知指令: {cmd}")

    parsed = len(pixels)
    if parsed != expected:
        print(f"警告: 解析像素 {parsed} 与宽高乘积 {expected} 不一致")
        if parsed < expected:
            pixels.extend([(0, 0, 0)] * (expected - parsed))
        else:
            pixels = pixels[:expected]

    img = Image.new("RGB", (w, h))
    img.putdata(pixels)
    img.save(output_path)
