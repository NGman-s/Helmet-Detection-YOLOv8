from ultralytics import YOLO
import cv2 

model_path = 'E:/code/project/runs/detect/train4/weights/best.pt' 
model = YOLO(model_path)

source_image_path = 'E:/code/project/photo' 

results = model.predict(source=source_image_path, save=True, conf=0.5)

print(f"检测完成！结果已保存在最新的 'runs/detect/predictX' 文件夹中。")

for r in results:
    print("\n--- 图片信息 ---")
    print(f"图片路径: {r.path}")
    print(f"检测框数量: {len(r.boxes)}")
    
    for box in r.boxes:
        class_id = int(box.cls) 
        class_name = model.names[class_id] 
        confidence = float(box.conf) 
        coordinates = box.xyxy[0] 
        
        print(f"  - 类别: {class_name}, 置信度: {confidence:.2f}, 坐标: {coordinates}")

for r in results:
     im_array = r.plot()  
     cv2.imshow('YOLOv8 Detection', im_array)
     if cv2.waitKey(0) & 0xFF == ord('q'): 
         break
cv2.destroyAllWindows()