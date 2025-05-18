# Chip Detection System

A full-stack application for detecting and classifying chips in videos using YOLOv11s object detection. The system consists of a FastAPI backend for video processing and a React frontend for user interaction.

![image](https://github.com/user-attachments/assets/7de9feac-14c6-4460-b70f-6a060320879b)

![image](https://github.com/user-attachments/assets/b0c8e7f3-837d-47c5-a213-978d32b3d8b1)

![image](https://github.com/user-attachments/assets/e2aecfb3-147a-4b19-b2ea-c113d5986161)

## Features

- **Video Upload**: Upload MP4, AVI, MOV, or MKV files (up to 100MB)
- **Processing**: Process videos with YOLOv11s model
- **Visual Results**: View processed videos with bounding boxes and labels
- **Performance Metrics**: See detailed processing statistics
- **Responsive UI**: Clean, modern interface with intuitive controls
- **Automatic Cleanup**: Old processed videos are automatically removed

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- Ultralytics YOLOv11s
- OpenCV
- Uvicorn

### Frontend
- React 18
- TypeScript
- Axios
- Tailwind CSS (via PostCSS)

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- Yarn or npm

### Backend Setup
1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   ```bash
   cd CHIPS/backend
   pip install -r requirements.txt
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd CHIPS/frontend
   ```
2. Install dependencies:
   ```bash
   yarn install  # or npm install
   ```

## Usage

### Running the Backend
```bash
cd CHIPS/backend
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`

### Running the Frontend
```bash
cd CHIPS/frontend
yarn start  # or npm start
```
The application will open at `http://localhost:3000`

## API Endpoints

- `POST /detect_chips/`: Upload a video for processing
- `GET /processed_videos/{filename}`: Download processed videos
- `GET /health`: Health check endpoint

## Project Structure

```
chip-detection/
├── backend/                  # FastAPI application
│   ├── app/                  
│   │   ├── main.py           # Main application file
│   ├── model/                # YOLO model weights
│   ├── uploads/              # Temporary upload storage
│   ├── processed/            # Processed videos storage
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # React application
│   ├── public/               # Static assets
│   ├── src/                  # Application source
│   │   ├── App.tsx           # Main component
│   │   ├── App.css           # Main styles
│   │   └── index.tsx         # Entry point
│   └── package.json          # Node dependencies
│
└── README.md                 # This file
```

## Acknowledgments

- Ultralytics for YOLOv8
- FastAPI and React communities
- OpenCV for video processing
