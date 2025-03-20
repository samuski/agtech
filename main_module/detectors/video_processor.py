import os
import cv2
from .leaf_detector import get_leaf_detector

def process_video(video_path, frames_output_dir, detector=None):
    """
    Processes a video by extracting frames, running object detection on each frame,
    and saving annotated frames to frames_output_dir.
    
    Args:
      video_path (str): Path to the input video file.
      frames_output_dir (str): Directory where annotated frames will be saved.
      detector: An object detector instance (if None, a default is loaded).
    
    Returns:
      tuple: (list of annotated frame file paths, frames per second of the video)
    """
    if detector is None:
        detector = get_leaf_detector()  # Load default YOLOv5 model (or your custom one)
    
    if not os.path.exists(frames_output_dir):
        os.makedirs(frames_output_dir)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: could not open video file", video_path)
        return [], 0.0

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = 0
    annotated_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect(frame)
        # Draw detections on the frame
        for det in detections:
            x, y, w, h = det['bbox']
            label = f"{det['label']} {det['confidence']:.2f}"
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        output_filename = os.path.join(frames_output_dir, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(output_filename, frame)
        annotated_frames.append(output_filename)
        frame_number += 1

    cap.release()
    return annotated_frames, fps

def reassemble_video(frames_dir, output_video_path, fps):
    """
    Reassembles annotated frames into a video.
    
    Args:
      frames_dir (str): Directory containing annotated frame images.
      output_video_path (str): Path to save the output video.
      fps (float): Frames per second for the output video.
      
    Returns:
      bool: True if video reassembly is successful, False otherwise.
    """
    import glob
    frame_files = sorted(glob.glob(os.path.join(frames_dir, 'frame_*.jpg')))
    if not frame_files:
        return False
    first_frame = cv2.imread(frame_files[0])
    height, width, _ = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    for frame_file in frame_files:
        frame = cv2.imread(frame_file)
        out.write(frame)
    out.release()
    return True
