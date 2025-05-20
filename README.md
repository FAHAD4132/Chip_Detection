# Chip Detection System

A full-stack application for detecting and classifying chips in videos using YOLOv11s object detection. The system consists of:
- Custom-trained YOLOv11s model for chip detection
- FastAPI backend for video processing
- React frontend for user interaction

![image](https://github.com/user-attachments/assets/7de9feac-14c6-4460-b70f-6a060320879b)

![image](https://github.com/user-attachments/assets/b0c8e7f3-837d-47c5-a213-978d32b3d8b1)

![image](https://github.com/user-attachments/assets/e2aecfb3-147a-4b19-b2ea-c113d5986161)

## Features

### Detection Model
- **Custom-trained YOLOv11s model** specifically for chip detection
- **200+ annotated images** covering various chip types and scenarios
- **60 training epochs** for optimal performance
- **640x640 resolution** for detailed detection

### Application Features
- **Video Upload**: Upload MP4, AVI, MOV, or MKV files (up to 100MB)
- **Processing**: Process videos with YOLOv11s model
- **Visual Results**: View processed videos with bounding boxes and labels
- **Performance Metrics**: See detailed processing statistics
- **Responsive UI**: Clean, modern interface with intuitive controls
- **Automatic Cleanup**: Old processed videos are automatically removed

## Model Training Details

### Dataset Preparation
- **200 custom images** captured with:
  - Different chip types and orientations
  - Mixed with random objects
  - Varied backgrounds and lighting conditions
- **Labeling** done with Label Studio
- **90-10 train-validation split**

![Screenshot of labal studio](https://github.com/user-attachments/assets/61f0546b-5f90-4ac4-b54c-b23ab31b6299)

```yaml
# Dataset configuration (data.yaml)
path: /content/data
train: train/images
val: validation/images
nc: 1  # Number of classes
names: ['albatal_dubbi_corn_snack',
        'albatal_popcorn_butter_flavor',
        'cric_crac_special_flavour',
        'cric_crac_tomato_ketchup',
        'marami_hot_chili',
        'marami_salt_&_vinegar',
        'tasali_hot_chili']  # Class name
```

### Training Process
```bash
# Training command
!yolo detect train data=/content/data.yaml model=yolo11s.pt epochs=60 imgsz=640
```
- **Model Architecture**: YOLOv11s small variant (optimal balance of speed/accuracy)
- **Training Duration**: 60 epochs (complete passes through dataset)
- **Image Resolution**: 640x640 pixels
- **Key Metrics Monitored**:
  - Box loss (localization accuracy)
  - Cls loss (classification accuracy)
  - DFL loss (distribution focal loss)

### Performance Metrics

#### Training Summary
- **Model**: YOLOv11s
- **Epochs**: 60
- **Training Time**: 0.173 hours (~10.4 minutes)
- **GPU**: Tesla T4 (15GB VRAM)
- **Image Size**: 640×640 pixels
- **Batch Size**: 16
- **Optimizer**: AdamW (auto-configured)
- **Final Model Size**: 19.2MB

#### Key Metrics Evolution
| Epoch Range | Box Loss | Class Loss | DFL Loss | mAP50 | mAP50-95 |
|-------------|----------|------------|----------|-------|----------|
| 1-10        | 0.76→0.51 | 3.46→0.55 | 1.10→0.93 | 0.32→0.92 | 0.31→0.81 |
| 11-20       | 0.51→0.47 | 0.52→0.45 | 0.94→0.92 | 0.92→0.97 | 0.81→0.93 |
| 21-30       | 0.48→0.44 | 0.45→0.39 | 0.94→0.91 | 0.96→0.99 | 0.89→0.95 |
| 31-40       | 0.43→0.37 | 0.37→0.31 | 0.91→0.90 | 0.99→1.00 | 0.93→0.97 |
| 41-50       | 0.37→0.35 | 0.31→0.29 | 0.90→0.89 | 0.99→1.00 | 0.96→0.99 |
| 51-60       | 0.24→0.20 | 0.22→0.18 | 0.78→0.77 | 1.00→1.00 | 0.98→0.99 |

#### Final Validation Metrics (Epoch 60)
| Metric       | Value   |
|--------------|---------|
| **Precision** | 0.992   |
| **Recall**    | 1.000   |
| **mAP50**     | 0.995   |
| **mAP50-95**  | 0.987   |
| **Inference Speed** | 7.1ms/img |

#### Class-wise Performance
| Chip Type                  | Precision | Recall | mAP50 | mAP50-95 |
|----------------------------|-----------|--------|-------|----------|
| albatal_dubbi_corn_snack   | 0.992     | 1.000  | 0.995 | 0.984    |
| albatal_popcorn_butter_flavor | 0.989  | 1.000  | 0.995 | 0.995    |
| cric_crac_special_flavour  | 0.992     | 1.000  | 0.995 | 0.995    |
| cric_crac_tomato_ketchup   | 0.980     | 1.000  | 0.995 | 0.983    |
| marami_hot_chili           | 0.985     | 1.000  | 0.995 | 0.995    |
| marami_salt_&_vinegar      | 0.995     | 1.000  | 0.995 | 0.966    |
| tasali_hot_chili           | 0.993     | 1.000  | 0.995 | 0.995    |


### Model Export
- Saved as `chip_detector.pt`
- Includes:
  - Optimized weights
  - Training logs
  - Configuration files
  - Sample predictions

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
├── backend/                                       # FastAPI application
│   ├── app/                  
│   │   └── main.py                                # Main application file
│   ├── model/                
│   │   └── chip_detector.pt                       # Trained weights
│   ├── uploads/                                   # Temporary upload storage
│   ├── processed/                                 # Processed videos storage
│   └── requirements.txt                           # Python dependencies
│
└── frontend/                                      # React application
    ├── public/                                    # Static assets
    ├── src/                                       # Application source
    │   ├── App.tsx                                # Main component
    │   ├── App.css                                # Main styles
    │   └── index.tsx                              # Entry point
    └── package.json                               # Node dependencies

Train_model/                                       # Model training workspace
├── content/                                       # data 
│   ├── custom_data/                               # Raw dataset before processing
│   │   ├── images/                                # Original jpg images (200+ samples)
│   │   ├── labls/                                 # YOLO format annotations (.txt files)
│   │   └── classes.txt                            # Label definitions (7 chip classes)
│   │
│   ├── data/                                      # Processed training data
│   │   ├── train/                                 # Training split (90%)
│   │   │   ├── images/                            # Training images
│   │   │   └── labels/                            # Corresponding labels
│   │   └── validation/                            # Validation split (10%)
│   │       ├── images/                            # Validation images
│   │       └── labels/                            # Corresponding labels
│   │
│   ├── my_model/                                  # Final exported model package
│   │   ├── training_results/                      # Complete training artifacts
│   │   │   ├── weights/                           # Model checkpoints
│   │   │   │   ├── best.pt                        # Best performing weights
│   │   │   │   └── last.pt                        # Final epoch weights
│   │   │   ├── args.yaml
│   │   │   ├── confusion_matrix.png               # Evaluation plots
│   │   │   ├── confusion_matrix_normalized.png    # Evaluation plots
│   │   │   ├── F1_curve.png                       # Evaluation plots
│   │   │   ├── labels.jpg                         # Sample detection visualizations
│   │   │   ├── P_curve.png                        # Evaluation plots
│   │   │   ├── PR_curve.png                       # Evaluation plots
│   │   │   ├── R_curve.png                        # Evaluation plots
│   │   │   ├── results.excel                      # Training metrics 
│   │   │   ├── results.png                        # Training metrics 
│   │   │   ├── train_batch0.jpg                   # Sample detection visualizations
│   │   │   ├── train_batch1.jpg                   # Sample detection visualizations
│   │   │   ├── train_batch2.jpg                   # Sample detection visualizations
│   │   │   ├── train_batch600.jpg                 # Sample detection visualizations
│   │   │   ├── train_batch601.jpg                 # Sample detection visualizations
│   │   │   ├── train_batch602.jpg                 # Sample detection visualizations
│   │   │   ├── val_batch0_labels.jpg              # Sample detection visualizations
│   │   │   └── val_batch0_pred.jpg                # Sample detection visualizations
│   │   └── chip_detector.pt                       # production weights
│   │
│   ├── runs/                                      # Training runtime outputs
│   │   └── detect/
│   │       ├── train/                             # Identical to my_model/training_results
│   │       │   ├── weights/
│   │       │   │   ├── best.pt
│   │       │   │   └── last.pt
│   │       │   ├── args.yaml
│   │       │   ├── confusion_matrix.png
│   │       │   ├── confusion_matrix_normalized.png
│   │       │   ├── F1_curve.png
│   │       │   ├── labels.jpg
│   │       │   ├── P_curve.png
│   │       │   ├── PR_curve.png
│   │       │   ├── R_curve.png
│   │       │   ├── results.excel
│   │       │   ├── results.png
│   │       │   ├── train_batch0.jpg
│   │       │   ├── train_batch1.jpg
│   │       │   ├── train_batch2.jpg
│   │       │   ├── train_batch600.jpg
│   │       │   ├── train_batch601.jpg
│   │       │   ├── train_batch602.jpg
│   │       │   ├── val_batch0_labels.jpg
│   │       │   └── val_batch0_pred.jpg
│   │       └── predict/                           # Prediction outputs (not used in production)
│   │
│   ├── chip_detector.zip/                         # Compressed model package for distribution
│   │   ├── training_results/
│   │   │   ├── weights/
│   │   │   │   ├── best.pt
│   │   │   │   └── last.pt
│   │   │   ├── args.yaml
│   │   │   ├── confusion_matrix.png
│   │   │   ├── confusion_matrix_normalized.png
│   │   │   ├── F1_curve.png
│   │   │   ├── labels.jpg
│   │   │   ├── P_curve.png
│   │   │   ├── PR_curve.png
│   │   │   ├── R_curve.png
│   │   │   ├── results.excel
│   │   │   ├── results.png
│   │   │   ├── train_batch0.jpg
│   │   │   ├── train_batch1.jpg
│   │   │   ├── train_batch2.jpg
│   │   │   ├── train_batch600.jpg
│   │   │   ├── train_batch601.jpg
│   │   │   ├── train_batch602.jpg
│   │   │   ├── val_batch0_labels.jpg
│   │   │   └── val_batch0_pred.jpg
│   │   └── chip_detector.pt
│   │
│   └── data.yaml                                  # YOLO dataset configuration file
│
├── data.zip/                                      # Original dataset archive               
│   ├── images/                                    # All input images
│   ├── labls/                                     # YOLO annotation text files
│   └── classes.txt                                # List of chip classes
│
├── Notebook_Images/                               # Documentation assets
│   ├── processed.mp4                              # Sample detection video
│   └── Screenshot_of_labal_studio.png             # Annotation example
│
├── Chip_Detections.ipynb                          # Complete training notebook
└── yolo11s.pt                                     # Pretrained YOLOv11s base model

README.md                                          # Project documentation (This file)
```

## Acknowledgments

- Ultralytics for YOLOv11s
- Label Studio for annotation tools
- FastAPI and React communities
- OpenCV for video processing
