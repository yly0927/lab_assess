import os
import sys
import time

from okti_decoder import decode_okti
from okti_encoder import encode_okti


def fail(message):
    print(message)
    sys.exit(1)


def main():
    if len(sys.argv) != 4:
        fail("错误：参数数量不正确。\n用法: python main.py <compress|decompress> <输入路径> <输出路径>")

    mode = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    if mode not in ("compress", "decompress"):
        fail("错误：模式必须为 compress 或 decompress")

    if not os.path.exists(input_path):
        fail(f"错误：找不到输入文件 {input_path}")

    start_time = time.time()

    try:
        if mode == "compress":
            encode_okti(input_path, output_path)
        else:
            decode_okti(input_path, output_path)
    except Exception as e:
        fail(f"运行失败：{e}")

    elapsed = time.time() - start_time
    in_size = os.path.getsize(input_path)
    out_size = os.path.getsize(output_path)

    print("-" * 30)
    if mode == "compress":
        print("压缩完成！")
        print(f"耗时: {elapsed:.4f} 秒")
        print(f"原始大小: {in_size} 字节")
        print(f"压缩后大小: {out_size} 字节")
        if in_size == 0:
            print("数据缩减量: 无法计算（输入文件为空）")
        elif out_size <= in_size:
            ratio = (1 - out_size / in_size) * 100
            print(f"数据缩减量: {ratio:.2f}%")
        else:
            ratio = (out_size / in_size - 1) * 100
            print(f"体积变化: 膨胀 {ratio:.2f}%")
    else:
        print("解压完成！")
        print(f"耗时: {elapsed:.4f} 秒")
    print("-" * 30)


if __name__ == "__main__":
    main()
