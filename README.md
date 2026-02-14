# AiGenics: Smart Waste Classification & Tracking

AiGenics is an end-to-end full-stack IoT computer vision pipeline. It utilizes a custom-trained YOLOv8 Nano model to identify and track waste categories in real-time, pushing aggregated telemetry data to a MERN stack command center for visual analytics.

## System Architecture
1. **Edge Inference (Python/OpenCV):** Captures live webcam feeds and runs a custom YOLO model (trained on the TACO dataset).
2. **Object Tracking (ByteTrack):** Implements multi-object tracking to assign unique, persistent IDs to individual items, preventing duplicate database entries for a single piece of waste.
3. **REST API (Express/Node.js):** Receives structured JSON payloads from the edge device.
4. **Database (MongoDB):** Stores relational data between physical Smart Bins and high-frequency waste logs.
5. **Dashboard (React/Vite/Recharts):** A responsive, auto-refreshing interface visualizing waste distribution analytics.

## Tech Stack
* **Computer Vision:** PyTorch, Ultralytics YOLOv8n, OpenCV, ByteTrack
* **Backend:** Node.js, Express.js, Mongoose
* **Frontend:** React, Vite, Recharts
* **Database:** MongoDB

## Local Setup & Installation

### 1. The MERN Backend
\`\`\`bash
cd backend
npm install
# Create a .env file with PORT=5000 and your MONGO_URI
node server.js
\`\`\`

### 2. The React Command Center
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

### 3. The Edge AI
Ensure you have Python installed and your virtual environment activated.
\`\`\`bash
pip install -r requirements.txt
# Update the BIN_OBJECT_ID in src/inference.py with your MongoDB SmartBin _id
python src/inference.py
\`\`\`

## Engineering Notes
* **Duplicate Log Mitigation:** Migrated from a brute-force time-based cooldown approach to implementing ByteTrack. This allows the system to establish object permanence, reliably tracking items across frames and ensuring a 1:1 ratio of physical objects to database entries.