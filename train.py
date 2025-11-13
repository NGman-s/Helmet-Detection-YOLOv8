from ultralytics import YOLO


model = YOLO('yolov8n.pt') 


if __name__ == '__main__':
   
    results = model.train(data='E:/code/project/SafetyHelmet_Kaggle/data.yaml', 
                          epochs=50, 
                          imgsz=640)