from ultralytics import YOLO

def train_aigenics_model():
    print("Initializing AiGenics YOLOv8 Training Pipeline...")

    # Load a pre-trained Nano model for fast inference on edge devices
    model = YOLO('yolov8n.pt') 

    # Train the model
    # Adjust 'epochs' and 'batch' based on your cloud environment's GPU memory
    results = model.train(
        data='data.yaml',       # Path to our config file
        epochs=50,              # Start with 50 to check for learning/overfitting
        batch=16,               # Standard batch size
        imgsz=640,              # Standard image size for YOLO
        name='aigenics_taco_v1',# Names the output folder in /runs
        device='0'              # Forces GPU usage (use 'cpu' if no GPU is available)
    )

    print("Training complete! Weights saved to runs/detect/aigenics_taco_v1/weights/")

if __name__ == '__main__':
    train_aigenics_model()