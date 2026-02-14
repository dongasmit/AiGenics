import json
import os

TARGET_CLASSES = ['Plastic', 'Metal', 'Paper', 'Glass', 'Trash']

# Mapping from TACO category names to our 5 target classes
TACO_CATEGORY_MAPPING = {
    # Plastic
    'Clear plastic bottle': 'Plastic',
    'Disposable plastic cup': 'Plastic',
    'Other plastic bottle': 'Plastic',
    'Other plastic cup': 'Plastic',
    'Plastic bottle cap': 'Plastic',
    'Plastic lid': 'Plastic',
    'Crisp packet': 'Plastic',
    'Disposable food container': 'Plastic',
    'Foam cup': 'Plastic',
    'Foam food container': 'Plastic',
    'Other plastic': 'Plastic',
    'Other plastic container': 'Plastic',
    'Other plastic wrapper': 'Plastic',
    'Plastic film': 'Plastic',
    'Plastic gloves': 'Plastic',
    'Plastic straw': 'Plastic',
    'Plastic utensils': 'Plastic',
    'Polypropylene bag': 'Plastic',
    'Single-use carrier bag': 'Plastic',
    'Spread tub': 'Plastic',
    'Squeezable tube': 'Plastic',
    'Styrofoam piece': 'Plastic',
    'Tupperware': 'Plastic',

    # Metal
    'Aerosol': 'Metal',
    'Aluminium foil': 'Metal',
    'Drink can': 'Metal',
    'Food can': 'Metal',
    'Metal bottle cap': 'Metal',
    'Metal lid': 'Metal',
    'Pop tab': 'Metal',
    'Scrap metal': 'Metal',

    # Paper
    'Carded blister pack': 'Paper',
    'Corrugated carton': 'Paper',
    'Egg carton': 'Paper',
    'Magazine paper': 'Paper',
    'Meal carton': 'Paper',
    'Normal paper': 'Paper',
    'Other carton': 'Paper',
    'Paper bag': 'Paper',
    'Paper cup': 'Paper',
    'Paper straw': 'Paper',
    'Pizza box': 'Paper',
    'Toilet tube': 'Paper',
    'Tissues': 'Paper',
    'Wrapping paper': 'Paper',

    # Glass
    'Broken glass': 'Glass',
    'Glass bottle': 'Glass',
    'Glass cup': 'Glass',
    'Glass jar': 'Glass',

    # Trash
    'Aluminium blister pack': 'Trash',
    'Battery': 'Trash',
    'Cigarette': 'Trash',
    'Drink carton': 'Trash',
    'Food waste': 'Trash',
    'Garbage bag': 'Trash',
    'Rope & strings': 'Trash',
    'Shoe': 'Trash',
    'Six-pack rings': 'Trash',
    'Unlabeled litter': 'Trash',
}

def convert_taco_to_yolo(coco_json_path, output_labels_dir):
    """Parses TACO JSON, normalizes coordinates, and writes YOLO txt files."""
    
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
        
    os.makedirs(output_labels_dir, exist_ok=True)
    
    # Extract image dimensions for normalization
    image_info = {img['id']: (img['width'], img['height']) for img in coco_data['images']}
    
    # Create a mapping from category_id to category_name
    category_id_to_name = {cat['id']: cat['name'] for cat in coco_data['categories']}

    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        category_id = ann['category_id']
        bbox = ann['bbox'] # COCO: [x_min, y_min, width, height]
        
        img_width, img_height = image_info[image_id]
        
        # Calculate YOLO normalized coordinates
        x_center = (bbox[0] + bbox[2] / 2) / img_width
        y_center = (bbox[1] + bbox[3] / 2) / img_height
        w_norm = bbox[2] / img_width
        h_norm = bbox[3] / img_height
        
        # Get category name and map to target class
        cat_name = category_id_to_name.get(category_id)
        target_class_name = TACO_CATEGORY_MAPPING.get(cat_name, 'Trash') # Default to Trash if unknown
        
        # Get target class index
        try:
            target_class_id = TARGET_CLASSES.index(target_class_name)
        except ValueError:
            print(f"Warning: mapped class '{target_class_name}' not found in TARGET_CLASSES.")
            continue

        # Format the line: <class_id> <x_center> <y_center> <width> <height>
        yolo_line = f"{target_class_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n"
        
        # Save to a .txt file matching the image name
        txt_filename = f"{image_id:06d}.txt" 
        txt_filepath = os.path.join(output_labels_dir, txt_filename)
        
        with open(txt_filepath, 'a') as txt_file:
            txt_file.write(yolo_line)

    print(f"Conversion complete. YOLO labels saved to {output_labels_dir}")  

# Example execution
# convert_taco_to_yolo('../data/TACO/annotations.json', '../data/labels/')