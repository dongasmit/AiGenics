from ultralytics import YOLO

def train_aigenics_model():
    print("Initializing AiGenics YOLO26 Training Pipeline...")

    # Load the new YOLO26 pre-trained Nano model
    model = YOLO('yolo26n.pt') 

    # Train the model
    results = model.train(
        data='data.yaml',       
        epochs=50,              
        batch=16,               
        imgsz=640,              
        name='aigenics_taco_v1',
        device='0'              # Using your cloud GPU
    )

    print("Training complete! Weights saved to runs/detect/aigenics_taco_v1/weights/")

if __name__ == '__main__':
    train_aigenics_model()