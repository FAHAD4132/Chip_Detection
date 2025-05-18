import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

interface ProcessingMetrics {
  total_frames: number;
  average_processing_time_per_frame: number;
  processing_fps: number;
  original_fps: number;
  resolution: string;
}

export default function ChipDetectionApp() {

  const [video, setVideo] = useState<File | null>(null);
  const [videoPreviewUrl, setVideoPreviewUrl] = useState<string | null>(null);
  const [processedVideo, setProcessedVideo] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [metrics, setMetrics] = useState<ProcessingMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showMetrics, setShowMetrics] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const previewVideoRef = useRef<HTMLVideoElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDownload = () => {
    if (!processedVideo) return;
    
    // Create a temporary anchor element to trigger download
    const link = document.createElement('a');
    link.href = processedVideo;
    
    // Extract filename from URL and set as download filename
    const filename = processedVideo.split('/').pop() || 'processed_video.mp4';
    link.setAttribute('download', filename);
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      
      // Validate file size (100MB limit)
      if (file.size > 100 * 1024 * 1024) {
        setError("File size too large. Maximum 100MB allowed.");
        return;
      }
      
      // Validate file type
      const validTypes = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-matroska'];
      if (!validTypes.includes(file.type)) {
        setError("Invalid file type. Please upload a video file (MP4, AVI, MOV, MKV).");
        return;
      }
      
      setVideo(file);
      setProcessedVideo(null);
      setMetrics(null);

      // Create preview URL
      const url = URL.createObjectURL(file);
      setVideoPreviewUrl(url);
    }
  };

  const clearSelection = () => {
    setVideo(null);
    setVideoPreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Clean up object URLs when component unmounts
  useEffect(() => {
    return () => {
      if (videoPreviewUrl) {
        URL.revokeObjectURL(videoPreviewUrl);
      }
    };
  }, [videoPreviewUrl]);

  const handleUpload = async () => {
    if (!video) return;
    
    setLoading(true);
    setProgress(0);
    setError(null);
    
    const formData = new FormData();
    formData.append("video", video);

    let progressInterval: NodeJS.Timeout | null = null;

    try {
      // Simulate progress (in a real app, you might use websockets for real progress)
      progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 5, 90)); // Cap at 90% until completion
      }, 500);

      const response = await axios.post("http://localhost:8000/detect_chips/", formData);
      
      if (progressInterval) {
        clearInterval(progressInterval);
      }
      setProgress(100);
      
      setProcessedVideo(`http://localhost:8000/processed_videos/${response.data.processed_video}`);
      setMetrics(response.data.metrics);
      
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      if (progressInterval) {
        clearInterval(progressInterval);
      }
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || "Error processing video");
      } else {
        setError("An unexpected error occurred");
      }
      console.error("Error uploading video:", err);
    } finally {
      setLoading(false);
    }
  };

  // Auto-play video when it's loaded
  useEffect(() => {
    if (videoRef.current && processedVideo) {
      videoRef.current.load();
    }
  }, [processedVideo]);

  return (
    <div className="app-container">
      <div className="main-container">
        <div className="card">
          {/* Centered header */}
          <div className="header">
            <h1 className="header-title">Chip Detection System</h1>
            <p className="header-subtitle">Upload a video to detect and classify electronic components</p>
          </div>
          
          {/* Main content container */}
          <div className="content-container">
            {/* File Upload Section */}
            <div className={`upload-area ${videoPreviewUrl ? 'upload-area-active' : ''}`}>
              {!videoPreviewUrl ? (
                <div className="upload-area-empty">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="video/*"
                    onChange={handleFileChange}
                    className="hidden"
                    id="video-upload"
                  />
                </div>
              ) : (
                <div className="results-container">
                  <div className="results-card">
                    <div className="results-header">
                      <h2 className="results-title">Uploaded Video</h2>
                      <button 
                        onClick={clearSelection} 
                        className="remove-button"
                      >
                        <span>Delete Video</span>
                      </button>
                    </div>
                    <div className="video-container">
                      <video
                        ref={previewVideoRef}
                        controls
                        className="video-preview"
                        src={videoPreviewUrl}
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Error Message */}
            {error && (
              <div className="error-message">
                <div>
                  <p style={{ fontWeight: '500' }}>Error</p>
                  <p style={{ fontSize: '0.875rem' }}>{error}</p>
                </div>
              </div>
            )}

            {/* Progress Bar */}
            {loading && (
              <div className="progress-container">
                <div className="progress-text">
                  <span>Processing video...</span>
                  <span>{progress}%</span>
                </div>
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            )}

            {/* Action Button */}
            {videoPreviewUrl && !loading && !processedVideo && (
              <div style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
                <button
                  onClick={handleUpload}
                  className="action-button"
                >
                  <span>Detect Components</span>
                </button>
              </div>
            )}

            {/* Results Section */}
            {processedVideo && (
              <div className="results-container">
                <div className="results-card">
                  <div className="results-header">
                    <h2 className="results-title">
                      Detection Results
                    </h2>
                    <button
                      onClick={handleDownload}
                      className="download-button"
                    >
                      <span>Download</span>
                    </button>
                  </div>

                  <div className="video-container">
                    <video
                      ref={videoRef}
                      controls
                      className="processed-video"
                      autoPlay
                    >
                      <source src={processedVideo} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  </div>

                  {/* Metrics Section */}
                  {metrics && (
                    <div className="metrics-container">
                      <div 
                        className="metrics-header"
                        onClick={() => setShowMetrics(!showMetrics)}
                      >
                        <h3 className="metrics-title">
                          Processing Metrics
                        </h3>
                        <span className="metrics-toggle">
                          {showMetrics ? 'Hide details' : 'Show details'}
                        </span>
                      </div>
                      
                      {showMetrics && (
                        <div className="metrics-content">
                          <table className="metrics-table">
                            <thead>
                              <tr>
                                <th className="table-header" style={{ textAlign: 'left' }}>Metric</th>
                                <th className="table-header" style={{ textAlign: 'left' }}>Value</th>
                              </tr>
                            </thead>
                            <tbody>
                              {[
                                { label: "Resolution", value: metrics.resolution },
                                { label: "Original FPS", value: metrics.original_fps.toFixed(2) },
                                { label: "Processing FPS", value: metrics.processing_fps.toFixed(2) },
                                { label: "Total Frames", value: metrics.total_frames },
                                { label: "Frame Process Time", value: `${metrics.average_processing_time_per_frame.toFixed(4)}s` },
                                { label: "Video Duration", value: `${(metrics.total_frames / metrics.original_fps).toFixed(2)}s` },
                              ].map((metric, index) => (
                                <tr 
                                  key={index}
                                  className="table-row"
                                >
                                  <td className="table-cell table-cell-label">
                                    {metric.label}
                                  </td>
                                  <td className="table-cell table-cell-value">
                                    {metric.value}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}