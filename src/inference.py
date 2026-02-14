import cv2
import requests
from ultralytics import YOLO

def run_smart_bin_inference():
    print("Loading AiGenics Custom Weights...")
    model = YOLO('runs/detect/aigenics_taco_v13/weights/best.pt')
    API_URL = 'http://127.0.0.1:5000/api/waste'
    BIN_OBJECT_ID = "69904db6413916c82a5ea286"  

    cap = cv2.VideoCapture(0)
    
    # --- NEW TRACKING LOGIC ---
    # This set will permanently remember the unique ID of every piece of garbage it has already logged
    logged_track_ids = set()
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # Swap .predict() for .track() and enable persist=True
        # We use ByteTrack as it is extremely fast and perfect for edge devices
        results = model.track(frame, conf=0.5, persist=True, tracker="bytetrack.yaml", verbose=False)
        
        # Ensure YOLO actually tracked an object in this specific frame before extracting data
        if results[0].boxes.id is not None:
            
            # Extract tracking IDs, classes, and confidences
            boxes = results[0].boxes
            track_ids = boxes.id.int().cpu().tolist()
            classes = boxes.cls.int().cpu().tolist()
            confidences = boxes.conf.float().cpu().tolist()
            
            for track_id, cls, conf in zip(track_ids, classes, confidences):
                class_name = model.names[cls]
                
                # The Gatekeeper: If we have NEVER seen this exact piece of garbage before
                if track_id not in logged_track_ids:
                    payload = {
                        "binId": BIN_OBJECT_ID,
                        "detectedClass": class_name,
                        "confidence": conf
                    }
                    
                    try:
                        response = requests.post(API_URL, json=payload, timeout=2)
                        if response.status_code == 201:
                            print(f"SUCCESS: Logged {class_name} (Tracker ID: #{track_id})")
                            # Add the ID to the set so we never log it again
                            logged_track_ids.add(track_id)
                    except requests.exceptions.RequestException:
                        print("CONNECTION ERROR: Make sure Node.js is running.")

        # Draw the bounding boxes and tracking trails
        annotated_frame = results[0].plot()
        cv2.imshow("AiGenics Smart Bin Feed", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_smart_bin_inference()