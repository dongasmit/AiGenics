import cv2
import requests
from ultralytics import YOLO

def run_smart_bin_inference():
    print("Loading AiGenics Custom Weights...")
    # Load your trained model (Ensure this path matches your Colab/Terminal output)
    model = YOLO('runs/detect/aigenics_taco_v13/weights/best.pt')
    
    API_URL = 'http://127.0.0.1:5000/api/waste'
    
    # PASTE YOUR MONGODB COMPASS _id HERE
    BIN_OBJECT_ID = "69904db6413916c82a5ea286" 

    # Start the webcam feed
    cap = cv2.VideoCapture(0)
    frame_counter = 0
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # Run YOLO inference on the current frame
        results = model(frame, conf=0.5, verbose=False)
        
        # We only want to send a database request every 30 frames (approx 1 second)
        # Otherwise, the script will spam your backend with 30 requests per second!
        if frame_counter % 30 == 0:
            for r in results:
                for box in r.boxes:
                    class_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[class_id]
                    
                    # Prepare the data payload
                    payload = {
                        "binId": BIN_OBJECT_ID,
                        "detectedClass": class_name,
                        "confidence": conf
                    }
                    
                    try:
                        # Fire the POST request to your Node.js server
                        response = requests.post(API_URL, json=payload, timeout=2)
                        if response.status_code == 201:
                            print(f"SUCCESS: Logged 1 piece of {class_name} to database!")
                    except requests.exceptions.RequestException as e:
                        print(f"CONNECTION ERROR: Make sure your Node.js server is running.")
        
        # Draw the bounding boxes and show the live video feed
        annotated_frame = results[0].plot()
        cv2.imshow("AiGenics Smart Bin Feed", annotated_frame)
        
        frame_counter += 1
        
        # Press 'q' to quit the webcam feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_smart_bin_inference()