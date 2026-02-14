import json
import os
import shutil
from src.data_pipeline import convert_taco_to_yolo, TARGET_CLASSES

# Mock Data
MOCK_COCO_DATA = {
    "images": [
        {"id": 1, "width": 1000, "height": 1000, "file_name": "img1.jpg"},
        {"id": 2, "width": 800, "height": 600, "file_name": "img2.jpg"}
    ],
    "categories": [
        {"id": 10, "name": "Clear plastic bottle"},
        {"id": 20, "name": "Drink can"},
        {"id": 30, "name": "Normal paper"},
        {"id": 40, "name": "Glass bottle"},
        {"id": 50, "name": "Cigarette"},
        {"id": 99, "name": "Unknown Item"}, # Should map to Trash
    ],
    "annotations": [
        # Image 1
        {"id": 1, "image_id": 1, "category_id": 10, "bbox": [100, 100, 200, 200]}, # Plastic
        {"id": 2, "image_id": 1, "category_id": 20, "bbox": [400, 400, 100, 100]}, # Metal
        # Image 2
        {"id": 3, "image_id": 2, "category_id": 30, "bbox": [50, 50, 100, 100]}, # Paper
        {"id": 4, "image_id": 2, "category_id": 40, "bbox": [200, 200, 50, 50]}, # Glass
        {"id": 5, "image_id": 2, "category_id": 50, "bbox": [300, 300, 20, 20]}, # Trash
        {"id": 6, "image_id": 2, "category_id": 99, "bbox": [400, 400, 50, 50]}, # Trash (fallback)
    ]
}

def test_conversion():
    # Setup
    test_dir = "test_output"
    os.makedirs(test_dir, exist_ok=True)
    json_path = os.path.join(test_dir, "mock_annotations.json")
    labels_dir = os.path.join(test_dir, "labels")
    
    with open(json_path, 'w') as f:
        json.dump(MOCK_COCO_DATA, f)
        
    # Run Conversion
    convert_taco_to_yolo(json_path, labels_dir)
    
    # Verify Content
    # Image 1: Plastic (0), Metal (1)
    file1 = os.path.join(labels_dir, "000001.txt")
    with open(file1, 'r') as f:
        lines = f.readlines()
        print(f"File 1 content:\n{''.join(lines)}")
        assert lines[0].startswith("0 "), "First object should be Plastic (0)"
        assert lines[1].startswith("1 "), "Second object should be Metal (1)"

    # Image 2: Paper (2), Glass (3), Trash (4), Trash (4)
    file2 = os.path.join(labels_dir, "000002.txt")
    with open(file2, 'r') as f:
        lines = f.readlines()
        print(f"File 2 content:\n{''.join(lines)}")
        assert lines[0].startswith("2 "), "First object should be Paper (2)"
        assert lines[1].startswith("3 "), "Second object should be Glass (3)"
        assert lines[2].startswith("4 "), "Third object should be Trash (4)"
        assert lines[3].startswith("4 "), "Fourth object should be Trash (4) (fallback)"

    print("All tests passed!")

    # Cleanup
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_conversion()
