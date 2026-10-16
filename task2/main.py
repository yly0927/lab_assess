import sys
import os
import time
from okti_encoder import encode_okti
from okti_decoder import decode_okti

def main():
    if len(sys.argv) != 4:
        print("错误：参数数量不正确。")
        print("用法: python main.py <compress|decompress> <输入路径> <输出路径>")
        return

    mode = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    # 1. 非法输入校验：检查输入文件是否存在
    if not os.path.exists(input_path):
        print(f"错误：找不到输入文件 {input_path}")
        return

    # 2. 开始计时
    start_time = time.time()

    # 3. 执行核心逻辑（包含异常捕获）
    try:
        if mode == "compress":
            encode_okti(input_path, output_path)
        elif mode == "decompress":
            decode_okti(input_path, output_path)
        else:
            print("错误：模式必须为 compress 或 decompress")
            return
    except Exception as e:
        print(f"运行失败：{e}")
        return

    # 4. 结束计时并计算耗时
    end_time = time.time()
    elapsed = end_time - start_time

    # 5. 获取文件大小并计算压缩率
    in_size = os.path.getsize(input_path)
    out_size = os.path.getsize(output_path)

    # 6. 输出运行统计信息
    if mode == "compress":
        ratio = (1 - out_size / in_size) * 100
        print("-" * 30)
        print("压缩完成！")
        print(f"耗时: {elapsed:.4f} 秒")
        print(f"原始大小: {in_size} 字节")
        print(f"压缩后大小: {out_size} 字节")
        print(f"数据缩减量: {ratio:.2f}%")
        print("-" * 30)
    else:
        print("-" * 30)
        print("解压完成！")
        print(f"耗时: {elapsed:.4f} 秒")
        print("-" * 30)

if __name__ == "__main__":
    main()