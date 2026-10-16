# okti_decoder.py
from PIL import Image

def decode_okti(okti_path, output_path):
    with open(okti_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines or lines[0] != "okti":
        raise ValueError("文件头不是 okti")

    ptr = 1
    w, h = map(int, lines[ptr].split())
    ptr += 1

    pixels = []
    pending_repeat = 1

    while ptr < len(lines):
        cmd = lines[ptr]
        ptr += 1
        
        if not cmd:
            continue

        c = cmd[0]

        if c == 'p':
            num_str = cmd[1:]
            if len(num_str) != 6:
                raise ValueError(f"颜色格式错误: {cmd}")
            
            r = int(num_str[0:2], 16)
            g = int(num_str[2:4], 16)
            b = int(num_str[4:6], 16)
            current_color = (r, g, b)
            
            pixels.extend([current_color] * pending_repeat)
            pending_repeat = 1
            
        elif c == 'n':
            num_str = cmd[1:]
            if not num_str:
                 raise ValueError(f"缺少重复次数: {cmd}")
            pending_repeat = int(num_str, 16)
            
        else:
            raise ValueError(f"未知指令: {cmd}")

    img = Image.new("RGB", (w, h))
    img.putdata(pixels[:w*h])
    img.save(output_path)