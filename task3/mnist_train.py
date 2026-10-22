import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 1. 设置超参数
BATCH_SIZE = 64
EPOCHS = 5
LEARNING_RATE = 0.001

# 2. 数据预处理与加载
# ToTensor() 把图片转为张量，Normalize() 进行标准化（均值0.1307，标准差0.3081是MNIST的通用值）
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# 注意：这里已经把 download 改成了 False，程序会直接读取本地 raw 文件夹里的文件
train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST('./data', train=False, download=True, transform=transform)

# 加载数据
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# 3. 定义卷积神经网络模型 (简单的 LeNet 结构)
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # 第一个卷积层：输入1通道(灰度图)，输出16通道，卷积核3x3
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2) # 池化后大小变为 14x14
        
        # 第二个卷积层：输入16通道，输出32通道
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2) # 池化后大小变为 7x7
        
        # 全连接层
        self.fc1 = nn.Linear(32 * 7 * 7, 128) # 将 32个 7x7 的特征图展平
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(128, 10) # 最终输出10个类别 (0-9)

    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = x.view(-1, 32 * 7 * 7) # 展平操作，-1表示自动计算batch_size
        x = self.relu3(self.fc1(x))
        x = self.fc2(x)
        return x

# 4. 初始化模型、损失函数和优化器
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"当前使用的设备: {device}")
model = SimpleCNN().to(device)
criterion = nn.CrossEntropyLoss() # 多分类常用的交叉熵损失
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# 5. 开始训练
print("开始训练模型...")
for epoch in range(EPOCHS):
    model.train() # 切换到训练模式
    running_loss = 0.0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()   # 清空梯度
        output = model(data)    # 前向传播
        loss = criterion(output, target) # 计算损失
        loss.backward()         # 反向传播
        optimizer.step()        # 更新权重
        
        running_loss += loss.item()
        
    print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {running_loss/len(train_loader):.4f}")

# 6. 在测试集上评估准确率
print("开始测试模型...")
model.eval() # 切换到评估模式
correct = 0
total = 0
with torch.no_grad(): # 测试时不需要计算梯度
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        outputs = model(data)
        _, predicted = torch.max(outputs.data, 1) # 取概率最大的类别作为预测结果
        total += target.size(0)
        correct += (predicted == target).sum().item()

accuracy = 100 * correct / total
print(f"测试集准确率: {accuracy:.2f}%")