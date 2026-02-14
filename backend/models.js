const mongoose = require('mongoose');

// 1. Smart Bin Schema (The physical hardware)
const smartBinSchema = new mongoose.Schema({
    binId: { type: String, required: true, unique: true },
    location: { type: String, required: true },
    fillLevel: { type: Number, default: 0 }, // 0 to 100 percentage
    status: { type: String, enum: ['Active', 'Maintenance', 'Full'], default: 'Active' }
}, { timestamps: true });

// 2. Waste Log Schema (The YOLO detections)
const wasteLogSchema = new mongoose.Schema({
    binId: { type: mongoose.Schema.Types.ObjectId, ref: 'SmartBin', required: true },
    detectedClass: {
        type: String,
        enum: ['Plastic', 'Metal', 'Paper', 'Glass', 'Trash'],
        required: true
    },
    confidence: { type: Number, required: true } // YOLO confidence score
}, { timestamps: true });

module.exports = {
    SmartBin: mongoose.model('SmartBin', smartBinSchema),
    WasteLog: mongoose.model('WasteLog', wasteLogSchema)
};