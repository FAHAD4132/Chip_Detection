from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import torch
import cv2
import numpy as np
import shutil
import os
from pathlib import Path
from ultralytics import YOLO
from fastapi.middleware.cors import CORSMiddleware
import uuid
from typing import Optional
from datetime import datetime
import logging
import time
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Chip Detection API",
              description="API for detecting chips in videos using YOLOv8",
              version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"
ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Color palette for different chip types
COLOR_PALETTE = {
    "albatal_dubbi_corn_snack": (255, 165, 0),      # Orange
    "albatal_popcorn_butter_flavor": (255, 223, 0), # Gold
    "cric_crac_special_flavour": (0, 128, 255),     # Blue
    "cric_crac_tomato_ketchup": (255, 0, 0),        # Red
    "marami_hot_chili": (139, 0, 0),               # Dark Red
    "marami_salt_&_vinegar": (0, 255, 255),        # Cyan
    "tasali_hot_chili": (128, 0, 128),             # Purple
    "default": (255, 255, 255)                     # White
}

# Load YOLOv11s model
try:
    model_path = "model/chips_model.pt" 
    model = YOLO(model_path)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise

def is_video_file(filename: str) -> bool:
    """Check if the file has a valid video extension."""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename with timestamp and UUID."""
    ext = Path(original_filename).suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{unique_id}{ext}"

def cleanup_old_videos():
    "Remove videos older than one hour"
    while True:
        try:
            now = time.time()
            for filename in os.listdir(PROCESSED_DIR):
                file_path = os.path.join(PROCESSED_DIR, filename)
                file_age = now - os.path.getmtime(file_path)
                
                # If the file is more than an hour (3600 seconds)
                if file_age > 3600:
                    try:
                        os.remove(file_path)
                        logger.info(f"The old file has been deleted: {filename}")
                    except Exception as e:
                        logger.error(f"Error deleting file {filename}: {str(e)}")
            
            # Wait 5 minutes before the next scan.
            time.sleep(300)
        except Exception as e:
            logger.error(f"Cleaning error: {str(e)}")
            time.sleep(60)

@app.post("/detect_chips/")
async def detect_chips(video: UploadFile = File(...)):
    """Endpoint for processing videos to detect chips."""
    # Validate file
    if not is_video_file(video.filename):
        raise HTTPException(status_code=400, detail="Invalid file format. Only video files are allowed.")
    
    # Generate unique filenames to prevent collisions
    unique_filename = generate_unique_filename(video.filename)
    video_path = os.path.join(UPLOAD_DIR, unique_filename)
    processed_video_path = os.path.join(PROCESSED_DIR, f"processed_{unique_filename}")
    
    try:
        # Save uploaded video with chunked writing for large files
        with open(video_path, "wb") as buffer:
            while chunk := await video.read(8192):  # 8KB chunks
                buffer.write(chunk)
        
        # Process video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Failed to open video file")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Initialize video 
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(
            processed_video_path, 
            fourcc, 
            fps, 
            (frame_width, frame_height),
            isColor=True
        )
        
        frame_count = 0
        processing_times = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            start_time = datetime.now()
            results = model(frame)
            processing_time = (datetime.now() - start_time).total_seconds()
            processing_times.append(processing_time)
            
            # Draw bounding boxes with labels
            for result in results:
                for box in result.boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Get class ID and confidence
                    class_id = int(box.cls)
                    confidence = float(box.conf)
                    
                    # Get class name (default to "chip" if names not available)
                    class_name = getattr(model, 'names', {}).get(class_id, "chip")

                    # Get color from palette or use default
                    color = COLOR_PALETTE.get(class_name, COLOR_PALETTE["default"])
                    
                    # Draw bounding box with shadow effect
                    thickness = 2
                    shadow_offset = 2
                    cv2.rectangle(frame, 
                                (x1 + shadow_offset, y1 + shadow_offset), 
                                (x2 + shadow_offset, y2 + shadow_offset), 
                                (50, 50, 50), thickness)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
                    
                    # Create label with class name and confidence
                    label = f"{class_name.upper()} {confidence:.2f}"
                    
                    # Calculate text size
                    (text_width, text_height), _ = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                    
                    # Draw label background with rounded corners
                    label_bg_top = y1 - text_height - 15
                    cv2.rectangle(frame, 
                                (x1 - 1, label_bg_top - 5), 
                                (x1 + text_width + 10, y1), 
                                color, -1)
                    
                    # Draw text with shadow
                    cv2.putText(frame, label, 
                                (x1 + 5, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                                (30, 30, 30), 2)  # Shadow
                    cv2.putText(frame, label, 
                                (x1 + 5, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                                (255, 255, 255), 1)  # White text
            
            out.write(frame)
            frame_count += 1
            
            # Log progress every 10% of the video
            if frame_count % (total_frames // 10) == 0:
                progress = (frame_count / total_frames) * 100
                logger.info(f"Processing: {progress:.1f}% complete")
        
        # Calculate metrics
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
        fps_processing = 1 / avg_processing_time if avg_processing_time > 0 else 0
        
        cap.release()
        out.release()
        
        # Clean up original file
        os.remove(video_path)

        # # Update the processd file time to start counting from now
        os.utime(processed_video_path, None)
        
        return {
            "status": "success",
            "processed_video": f"processed_{unique_filename}",
            "metrics": {
                "total_frames": frame_count,
                "average_processing_time_per_frame": avg_processing_time,
                "processing_fps": fps_processing,
                "original_fps": fps,
                "resolution": f"{frame_width}x{frame_height}"
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        # Clean up in case of error
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(processed_video_path):
            os.remove(processed_video_path)
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@app.get("/processed_videos/{video_filename}")
async def get_processed_video(video_filename: str):
    """Endpoint to retrieve processed videos."""
    video_path = os.path.join(PROCESSED_DIR, video_filename)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Update file time on each request to extend its lifetime
    os.utime(video_path, None)
    return FileResponse(video_path, media_type="video/mp4", filename=video_filename)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Start the cleaning thread when the application starts
cleanup_thread = Thread(target=cleanup_old_videos, daemon=True)
cleanup_thread.start()