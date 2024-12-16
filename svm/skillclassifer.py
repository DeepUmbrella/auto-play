import torch
import numpy as np
from torch import nn, optim
from abc import ABC, abstractmethod
from typing import Tuple
from enum import Enum

# 构造简单几何特征数据集


class BaseFeature():
    def __init__(self):
        pass

    @abstractmethod
    def feature(self) -> Tuple[float, float, float, float, float]:
        """Feature ,must be a tuple of 5 float  and must be implemented"""
        pass

    def mix_feature(self, other: 'BaseFeature') -> list:
        """混合特征"""
        if isinstance(other, BaseFeature):
            side, side_h, area, perimeter, compactness = self.feature()
            other_side, other_side_h, other_area, other_perimeter, other_compactness = other.feature()

            side_rate = self.side / other.side
            side_h_rate = self.side_h / other.side_h
            abs_compactness = abs(compactness - other_compactness)

            return [*self.feature(), *other.feature(), side_rate, side_h_rate, abs_compactness]
        else:
            raise TypeError("other must be a BaseFeature")


class DiaCircle(BaseFeature):

    def __init__(self, radius: int):
        super().__init__()
        self.radius = radius
        self.side = radius * 2
        self.side_h = radius * 2

    @property
    def perimeter(self):
        return 2 * np.pi * self.radius

    @property
    def area(self):
        return np.pi * self.radius ** 2

    @property
    def compactness(self):
        return 1.0

    def feature(self):
        return (self.side,
                self.side_h,
                self.area,
                self.perimeter,
                self.compactness
                )


class Rectangle(BaseFeature):

    def __init__(self, side: int, side_h=None):
        super().__init__()
        self.side = side
        self.side_h = side_h
        if side_h is None:
            self.side_h = side

    @property
    def perimeter(self):
        return 2 * (self.side + self.side_h)

    @property
    def area(self):
        return self.side * self.side_h

    @property
    def compactness(self):
        return (4 * np.pi * self.area) / (self.perimeter ** 2)

    def feature(self):
        return (self.side,
                self.side_h,
                self.area,
                self.perimeter,
                self.compactness)


class Adaptation():
    LOST_SMALL = 0
    SMALL = 1
    MEDIUM = 2
    FIT = 3
    More = 4
    Many = 5
    LOST_BIG = 6


show = [
    "LOST_SMALL",
    "SMALL",
    "MEDIUM",
    "FIT",
    "More",
    "Many",
    "LOST_BIG",
]

datasets = [

    (Rectangle(1068, 400), Rectangle(360, 175), Adaptation.LOST_BIG),
    (Rectangle(1068, 400), Rectangle(520, 200), Adaptation.LOST_BIG),
    (Rectangle(1068, 400), Rectangle(450, 200), Adaptation.LOST_BIG),
    (Rectangle(830, 250), Rectangle(360, 175), Adaptation.Many),
    (Rectangle(830, 250), Rectangle(360, 175), Adaptation.Many),
    (Rectangle(150, 110), Rectangle(600, 350), Adaptation.LOST_SMALL),
    (Rectangle(150, 110), Rectangle(360, 175), Adaptation.SMALL),
    (Rectangle(830, 250), Rectangle(360, 175), Adaptation.Many),
    (Rectangle(630, 300), Rectangle(450, 200), Adaptation.FIT),
    (Rectangle(360, 175), Rectangle(360, 175), Adaptation.FIT),
    (Rectangle(134, 107), Rectangle(360, 175), Adaptation.SMALL),
    (Rectangle(500, 300), Rectangle(400, 250), Adaptation.FIT),
    (Rectangle(370, 160), Rectangle(520, 280), Adaptation.MEDIUM),
    (Rectangle(580, 255), Rectangle(290, 150), Adaptation.Many),
    (Rectangle(600, 320), Rectangle(450, 150), Adaptation.More),
]


def generate_tensor_datasets(datasets: list[tuple[BaseFeature, BaseFeature, Adaptation]]) -> Tuple[np.ndarray, np.ndarray]:
    tensor_datasets = []
    adaptations = []
    for dataset in datasets:
        item, item1, adaptation = dataset
        tensor_datasets.append(item.mix_feature(item1))
        adaptations.append(adaptation)

    return np.array(tensor_datasets), np.array(adaptations)


class ShapeSimilarityModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ShapeSimilarityModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)  # 第一层全连接
        self.relu = nn.ReLU()                         # 激活函数
        self.fc2 = nn.Linear(hidden_size, output_size)  # 输出层
        self.sigmoid = nn.Sigmoid()                   # 将输出转为概率

    def forward(self, x):
        x = self.fc1(x)  # 输入 -> 第一层
        x = self.relu(x)  # 激活函数
        x = self.fc2(x)  # 第一层 -> 输出层
        x = self.sigmoid(x)  # 转为概率
        return x


if __name__ == "__main__":
    # 构造数据集
    X, y = generate_tensor_datasets(datasets)
    # 标签：0 = 不相似，1 = 相似

    # 转换为 PyTorch 张量
    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    # 初始化模型
    input_size = 13  # 输入特征数量（形状对特征）
    hidden_size = 10  # 隐藏层大小
    output_size = 7  # 输出（相似/不相似）
    model = ShapeSimilarityModel(input_size, hidden_size, output_size)
    criterion = nn.CrossEntropyLoss()   # 多分类交叉熵损失函数
    optimizer = optim.Adam(model.parameters(), lr=0.5)  # Adam 优化器

    num_epochs = 20000  # 训练轮数
    for epoch in range(num_epochs):
        # 前向传播
        outputs = model(X_tensor)
        loss = criterion(outputs, y_tensor)

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # 每隔 100 轮打印损失
        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

    model.eval()

    # 测试数据：新形状对
    test_data = torch.tensor(
        [Rectangle(400, 200).mix_feature(Rectangle(400, 150)),
         Rectangle(500, 200).mix_feature(Rectangle(472, 261))
         ], dtype=torch.float32)

    # 预测相似性
    with torch.no_grad():
        predicted_class = model(X_tensor)  # 输出形状为 [batch_size, num_classes]

# 获取每个样本的预测类别索引
        _, predicted_labels = torch.max(predicted_class, 1)

        # 输出预测类别的第一个样本的类别标签（假设 batch_size > 0）
        for item in predicted_labels:
            print("Predicted similarity:", show[item.item()])

    # 保存模型

    # torch.save(model.state_dict(), 'shape_similarity_model.pth')
