import os
import shutil
import random

def split_dataset(data_dir, split_ratio=0.8):
    print("Initializing dataset split...")
    
    # Define base paths
    images_dir = os.path.join(data_dir, 'images')
    labels_dir = os.path.join(data_dir, 'labels')
    
    # Create the train and val subdirectories
    for split in ['train', 'val']:
        os.makedirs(os.path.join(images_dir, split), exist_ok=True)
        os.makedirs(os.path.join(labels_dir, split), exist_ok=True)
        
    # Grab all image files (assuming TACO images are .jpg)
    images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(images)
    
    # Calculate the 80/20 split index
    split_idx = int(len(images) * split_ratio)
    train_images = images[:split_idx]
    val_images = images[split_idx:]
    
    # Helper function to move the paired images and labels
    def move_files(file_list, split_name):
        for img_name in file_list:
            # Move the image
            src_img = os.path.join(images_dir, img_name)
            dst_img = os.path.join(images_dir, split_name, img_name)
            shutil.move(src_img, dst_img)
            
            # Find and move the corresponding .txt label
            base_name = os.path.splitext(img_name)[0]
            label_name = f"{base_name}.txt"
            src_label = os.path.join(labels_dir, label_name)
            
            if os.path.exists(src_label):
                dst_label = os.path.join(labels_dir, split_name, label_name)
                shutil.move(src_label, dst_label)

    # Execute the moves
    move_files(train_images, 'train')
    move_files(val_images, 'val')
    
    print(f"Split complete! 80% Train ({len(train_images)}), 20% Val ({len(val_images)})")

if __name__ == '__main__':
    # Assuming your data folder is one level up from the src directory
    # Adjust this path if running directly in your cloud notebook root
    split_dataset('./data')