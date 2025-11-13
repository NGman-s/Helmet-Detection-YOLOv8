# 🚴‍♂️ 骑行帽检测系统 (Cycling Helmet Detection System)

基于YOLOv8的智能骑行帽检测系统，能够准确识别骑行者是否佩戴安全头盔。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📸 项目预览

本项目使用深度学习技术实现对骑行者的头盔佩戴情况进行实时检测，支持图片和视频流分析。

## 🎯 功能特性

- ✅ **实时检测**: 支持实时图片和视频中的头盔检测
- ✅ **高精度识别**: 基于YOLOv8模型，准确识别"佩戴头盔"和"未佩戴头盔"
- ✅ **批量处理**: 支持批量图片处理和视频流分析
- ✅ **可视化结果**: 检测结果实时显示，包含置信度和边界框
- ✅ **易于部署**: 完整的训练和推理代码，易于复现和部署

## 📊 模型性能

项目在BikesHelmets数据集上进行了训练，支持2个类别的检测：
- `With Helmet`: 佩戴头盔
- `Without Helmet`: 未佩戴头盔

## 🚀 快速开始

### 环境要求

- Python 3.8+
- PyTorch
- Ultralytics YOLOv8
- OpenCV
- NumPy
- tqdm

### 安装依赖

```bash
pip install -r requirements.txt
```

### 数据准备

1. 将你的数据集放在 `data/` 目录下，包含：
   - `data/images/`: 图片文件
   - `data/annotations/`: XML标注文件

2. 运行数据预处理：
```bash
python prepare_data.py
```

### 模型训练

```bash
python train.py
```

### 图片检测

```bash
python predict1.py
```

### 视频检测

```bash
python predict2.py
```

## 📁 项目结构

```
cycling-helmet-detection/
├── README.md                 # 项目说明文档
├── .gitignore               # Git忽略文件
├── requirements.txt         # 依赖包列表
├── train.py                # 训练脚本
├── prepare_data.py          # 数据预处理脚本
├── predict1.py             # 图片检测脚本
├── predict2.py             # 视频检测脚本
├── data.yaml               # 数据配置文件
├── yolov8n.pt              # YOLOv8预训练模型
├── data/                   # 原始数据集
│   ├── images/             # 图片文件
│   └── annotations/        # XML标注文件
├── SafetyHelmet_Kaggle/    # 处理后的YOLO格式数据
└── runs/                   # 训练和预测结果
```

## 🔧 使用说明

### 1. 数据预处理
`prepare_data.py` 会自动：
- 将XML标注转换为YOLO格式
- 划分训练集和验证集（8:2比例）
- 创建必要的目录结构
- 生成data.yaml配置文件

### 2. 模型训练
`train.py` 使用YOLOv8进行训练：
- 基于预训练模型yolov8n.pt
- 训练50个epochs
- 图片尺寸640x640
- 自动保存最佳模型权重

### 3. 检测功能

**图片检测** (`predict1.py`):
- 支持单张或批量图片检测
- 显示检测框和置信度
- 可视化检测结果

**视频检测** (`predict2.py`):
- 支持视频流处理
- 统计检测数量
- 保存检测结果

## 📈 训练结果

训练过程会产生丰富的可视化结果：
- 性能曲线（F1, PR, R曲线）
- 混淆矩阵
- 训练过程可视化
- 验证集检测结果

## 🎮 示例使用

```python
from ultralytics import YOLO

# 加载训练好的模型
model = YOLO('runs/detect/train4/weights/best.pt')

# 图片检测
results = model.predict(source='photo/', save=True, conf=0.5)

# 视频检测
video_results = model.predict(source='video/1.mp4', save=True, conf=0.5)
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📝 许可证

本项目基于MIT许可证开源。

## 🙏 致谢

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - 提供优秀的检测模型
- BikesHelmets数据集 - 提供训练数据

## 📧 联系方式

如果你有任何问题或建议，欢迎通过GitHub Issues联系。

---

⭐ 如果这个项目对你有帮助，请给它一个星标！