from ultralytics import YOLO
from pathlib import Path
import torch


if __name__ == "__main__":

    base_dir = Path.cwd()

    # 判断当前模型使用什么设备进行的训练
    if torch.cuda.is_available():

        print("当前设备为GPU")

    name = "jianmo"

    val_source_dir = f"{base_dir}/datasets/{name}/images/val"
    data_yaml = f"{base_dir}/datasets/{name}/data.yaml"

    # 1. 加载预训练模型（YOLOv8n 可以更换为 yolov8s, yolov8m 等）
    model = YOLO(f"{base_dir}/netmodels/yolov8/yolov8n.pt")  # 使用预训练模型

    # 2. 开始训练
    model.train(
        data=data_yaml,         # 数据集配置文件
        epochs=50,              # 训练轮数
        imgsz=640,              # 输入图片大小
        batch=16,               # 批量大小
        project="runs",         # 项目保存路径
        name=name,              # 自定义训练任务名称
        optimizer="Adam",       # 优化器 (可选：SGD, Adam, AdamW)
    )

    # 3. 评估模型
    metrics = model.val(data=data_yaml)  # 使用验证集评估性能
    print("评估结果:", metrics)

    # 4. 使用训练好的模型进行推理
    results = model.predict(
        source=val_source_dir,  # 推理的图片/视频路径
        conf=0.5,                     # 置信度阈值
        save=True,                    # 是否保存预测结果
    )

    # 5. 导出模型（可选：用于部署）
    # model.export(format="onnx")
