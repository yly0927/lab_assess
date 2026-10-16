import torch
import cv2
from PIL import Image
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
img = Image.open("test.jpg")
print("图像尺寸：", img.size)
img.show()


pip install pillow
from PIL import Image

def encode_okti(image: Image.Image, save_path: str):
    width, height = image.size
    pixels = list(image.getdata())

    lines = []
    lines.append("okti")
    lines.append(f"{width} {height}")

    for pix in pixels:
        r_hex = f"{pix[0]:02x}"
        g_hex = f"{pix[1]:02x}"
        b_hex = f"{pix[2]:02x}"
        lines.append(f"p{r_hex}{g_hex}{b_hex}")

    with open(save_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

    return {}


from PIL import Image

def decode_okti(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.readlines()
    ptr = 0
    magic = content[ptr].strip()
    ptr += 1
    if magic != "okti":
        raise ValueError("不是okti格式文件")

    w, h = map(int, content[ptr].strip().split())
    ptr +=1

    out_pixels = []
    while len(out_pixels) < w * h:
        line = content[ptr].strip()
        ptr +=1
        if not line:
            continue
        cmd = line[0]
        body = line[1:]
        if cmd == "p":
            rr = int(body[0:2], 16)
            gg = int(body[2:4], 16)
            bb = int(body[4:6], 16)
            out_pixels.append((rr, gg, bb))
        else:
            raise ValueError(f"暂不支持编码 {cmd}")

    im = Image.new("RGB", (w, h))
    im.putdata(out_pixels)
    return im, {}



import sys
from okt_encoder import encode_okti
from okt_decoder import decode_okti

def main():
    if len(sys.argv) <4:
        print("用法示例：")
        print("python main.py compress test/solid_red.png test/out.okti")
        print("python main.py decompress test/out.okti test/restore.png")
        return

    mode = sys.argv[1]
    in_path = sys.argv[2]
    out_path = sys.argv[3]

    if mode == "compress":
        from PIL import Image
        img = Image.open(in_path).convert("RGB")
        encode_okti(img, out_path)
        print(f"压缩完成，输出：{out_path}")
    elif mode == "decompress":
        img,_ = decode_okti(in_path)
        img.save(out_path)
        print(f"解压完成，输出：{out_path}")
    else:
        print("模式只能是 compress / decompress")

if __name__ == "__main__":
    main()

##压缩
python main.py compress test/solid_red.png test/out.okti
##解压
python main.py decompress test/out.okti test/restore.png
