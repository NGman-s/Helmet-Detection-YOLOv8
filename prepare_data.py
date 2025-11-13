import os
import random
import shutil
import xml.etree.ElementTree as ET
from tqdm import tqdm 

DATA_ROOT = 'E:/code/project/data' 


OUTPUT_ROOT = 'E:/code/project/SafetyHelmet_YOLO' 

CLASSES = {'With Helmet': 0, 'Without Helmet': 1}


TRAIN_RATIO = 0.8

def convert_xml_to_yolo(xml_file, output_txt_file, classes_map):
    """将单个XML文件转换为YOLO txt格式"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    size = root.find('size')
    if size is None: return # 跳过没有尺寸信息的xml

    img_width = int(size.find('width').text)
    img_height = int(size.find('height').text)

    with open(output_txt_file, 'w') as f:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name not in classes_map:
                continue # 如果类别不是我们需要的，就跳过
            
            class_id = classes_map[class_name]
            
            bndbox = obj.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)
            
            # 转换成YOLO格式 (center_x, center_y, width, height) 归一化
            x_center = (xmin + xmax) / 2.0 / img_width
            y_center = (ymin + ymax) / 2.0 / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height
            
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# prepare_data.py 的完整功能代码部分

def create_yolo_dataset():
    """主函数：创建YOLO数据集结构、转换并划分数据"""
    # 创建输出目录结构
    os.makedirs(os.path.join(OUTPUT_ROOT, 'images/train'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_ROOT, 'images/val'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_ROOT, 'labels/train'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_ROOT, 'labels/val'), exist_ok=True)
    
    xml_dir = os.path.join(DATA_ROOT, 'annotations')
    img_dir = os.path.join(DATA_ROOT, 'images')
    
    # 检查原始数据路径是否存在
    if not os.path.isdir(xml_dir):
        print(f"错误：找不到annotations文件夹，请检查路径: {xml_dir}")
        return
        
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    random.shuffle(xml_files) # 打乱文件顺序
    
    # --- 这一部分是关键，用来定义 train_files 和 val_files ---
    split_index = int(len(xml_files) * TRAIN_RATIO)
    train_files = xml_files[:split_index]
    val_files = xml_files[split_index:]
    # --- 关键部分结束 ---
    
    print(f"总文件数: {len(xml_files)}, 训练集: {len(train_files)}, 验证集: {len(val_files)}")
    
    print("正在处理训练集...")
    for xml_file in tqdm(train_files):
        base_name = os.path.splitext(xml_file)[0]
        
        possible_img_names = [base_name + '.png', base_name + '.jpg', base_name + '.jpeg']
        src_img_path = None
        img_file_name = None
        for name in possible_img_names:
            path_candidate = os.path.join(img_dir, name)
            if os.path.exists(path_candidate):
                src_img_path = path_candidate
                img_file_name = name
                break
        
        if src_img_path is None:
            # print(f"警告：找不到与 {xml_file} 匹配的图片，跳过") # 可以取消注释来查看跳过了哪些
            continue

        src_xml_path = os.path.join(xml_dir, xml_file)
        
        dst_img_path = os.path.join(OUTPUT_ROOT, 'images/train', img_file_name)
        shutil.copy(src_img_path, dst_img_path)
        
        dst_label_path = os.path.join(OUTPUT_ROOT, 'labels/train', base_name + '.txt')
        convert_xml_to_yolo(src_xml_path, dst_label_path, CLASSES)

    print("正在处理验证集...")
    for xml_file in tqdm(val_files):
        base_name = os.path.splitext(xml_file)[0]
        
        possible_img_names = [base_name + '.png', base_name + '.jpg', base_name + '.jpeg']
        src_img_path = None
        img_file_name = None
        for name in possible_img_names:
            path_candidate = os.path.join(img_dir, name)
            if os.path.exists(path_candidate):
                src_img_path = path_candidate
                img_file_name = name
                break
        
        if src_img_path is None:
            # print(f"警告：找不到与 {xml_file} 匹配的图片，跳过")
            continue

        src_xml_path = os.path.join(xml_dir, xml_file)
        
        dst_img_path = os.path.join(OUTPUT_ROOT, 'images/val', img_file_name)
        shutil.copy(src_img_path, dst_img_path)
        
        dst_label_path = os.path.join(OUTPUT_ROOT, 'labels/val', base_name + '.txt')
        convert_xml_to_yolo(src_xml_path, dst_label_path, CLASSES)
        
    # 创建 data.yaml 文件
    yaml_content = f"""
train: {os.path.join(OUTPUT_ROOT, 'images/train').replace('\\', '/')}
val: {os.path.join(OUTPUT_ROOT, 'images/val').replace('\\', '/')}

nc: {len(CLASSES)}
names: {list(CLASSES.keys())}
"""
    
    with open(os.path.join(OUTPUT_ROOT, 'data.yaml'), 'w') as f:
        f.write(yaml_content.strip())
        
    print("\n数据集准备完成！")
    print(f"YOLO格式的数据集已保存在: {OUTPUT_ROOT}")
    print(f"配置文件 'data.yaml' 已创建。")

# --- 主程序入口 ---
if __name__ == '__main__':
   
    DATA_ROOT = 'E:/code/project/data' 
    OUTPUT_ROOT = 'E:/code/project/SafetyHelmet_Kaggle' 
    
    if os.path.exists(OUTPUT_ROOT):
        print(f"发现旧的输出文件夹 {OUTPUT_ROOT}，正在删除...")
        shutil.rmtree(OUTPUT_ROOT)
        print("删除完成。")

    create_yolo_dataset()