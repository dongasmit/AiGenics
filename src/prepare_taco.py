import os
import json
import shutil
# Importing the mapping dictionaries you already wrote!
from data_pipeline import TARGET_CLASSES, TACO_CATEGORY_MAPPING

def prepare_taco_data():
    print("Flattening TACO images and generating YOLO labels...")
    taco_base = './data/TACO/data'
    json_path = os.path.join(taco_base, 'annotations.json')
    
    out_images_dir = './data/images'
    out_labels_dir = './data/labels'
    os.makedirs(out_images_dir, exist_ok=True)
    os.makedirs(out_labels_dir, exist_ok=True)
    
    with open(json_path, 'r') as f:
        coco_data = json.load(f)
        
    category_id_to_name = {cat['id']: cat['name'] for cat in coco_data['categories']}
    
    # 1. Move and rename images to a flat structure
    image_info = {}
    for img in coco_data['images']:
        src_img_path = os.path.join(taco_base, img['file_name']) 
        new_filename = f"{img['id']:06d}.jpg" # Standardizes the names to 000001.jpg
        dst_img_path = os.path.join(out_images_dir, new_filename)
        
        if os.path.exists(src_img_path):
            shutil.copy(src_img_path, dst_img_path)
            image_info[img['id']] = (img['width'], img['height'])
            
    # 2. Generate YOLO labels
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        if image_id not in image_info:
            continue
            
        category_id = ann['category_id']
        bbox = ann['bbox']
        img_width, img_height = image_info[image_id]
        
        # COCO to YOLO Math
        x_center = (bbox[0] + bbox[2] / 2) / img_width
        y_center = (bbox[1] + bbox[3] / 2) / img_height
        w_norm = bbox[2] / img_width
        h_norm = bbox[3] / img_height
        
        cat_name = category_id_to_name.get(category_id)
        target_class_name = TACO_CATEGORY_MAPPING.get(cat_name, 'Trash')
        
        try:
            target_class_id = TARGET_CLASSES.index(target_class_name)
        except ValueError:
            continue

        yolo_line = f"{target_class_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n"
        
        txt_filepath = os.path.join(out_labels_dir, f"{image_id:06d}.txt")
        with open(txt_filepath, 'a') as txt_file:
            txt_file.write(yolo_line)

    print(f"Data prepared! Images in {out_images_dir}, Labels in {out_labels_dir}")

if __name__ == '__main__':
    prepare_taco_data()