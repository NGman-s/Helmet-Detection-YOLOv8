from ultralytics import YOLO

model_path = 'E:/code/project/runs/detect/train4/weights/best.pt'
model = YOLO(model_path)

source_video_path = 'E:/code/project/video/1.mp4'

print("视频处理已开始，这可能需要一些时间，请耐心等待...")

results = model.predict(source=source_video_path, save=True, conf=0.5)

total_frames = 0
total_detections = 0
for r in results:
    total_frames += 1
    total_detections += len(r.boxes)

print("\n--- 处理结果总结 ---")
print(f"总共处理了 {total_frames} 帧。")
print(f"在所有帧中总共检测到 {total_detections} 个目标。")
print(f"视频检测完成！结果已保存在最新的 'runs/detect/predictX' 文件夹中。")