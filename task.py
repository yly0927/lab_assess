import torch
import cv2
from PIL import Image
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
img = Image.open("test.jpg")
print("图像尺寸：", img.size)
img.show()
