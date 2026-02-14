require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
// Importing the database blueprints we made in the last step
const { SmartBin, WasteLog } = require('./models');

const app = express();

// Middleware
// CORS allows your future React frontend to talk to this backend
app.use(cors()); 
// This allows the server to read the JSON data sent by the YOLO script
app.use(express.json()); 




// Database Connection
mongoose.connect(process.env.MONGO_URI)
.then(() => console.log('Successfully connected to MongoDB.'))
.catch(err => console.error('MongoDB connection error:', err));

// --- API ROUTES ---

// 1. THE INGESTION ROUTE: Where YOLO sends its predictions
app.post('/api/waste', async (req, res) => {
  try {
    const { binId, detectedClass, confidence } = req.body;
    
    const newLog = new WasteLog({
      binId,
      detectedClass,
      confidence
    });
    
    await newLog.save();
    res.status(201).json({ message: 'Waste logged successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to log waste', details: error.message });
  }
});

// 2. THE DASHBOARD ROUTE: Where your React app fetches the history
app.get('/api/logs', async (req, res) => {
  try {
    // .populate() automatically fetches the associated Smart Bin details!
    const logs = await WasteLog.find()
      .populate('binId')
      .sort({ createdAt: -1 })
      .limit(50);
      
    res.status(200).json(logs);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch logs' });
  }
});

// Boot up the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`AiGenics Command Center running on port ${PORT}`));