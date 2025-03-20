import os
from video_processing import process_video, reassemble_video

def main():
    # Path to your input video file
    # video_path = './media/WeChat_20250221230909.mp4'
    
    # print("Absolute video path:", os.path.abspath(video_path))
    # print("File exists:", os.path.exists(video_path))

    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    video_path = os.path.join(PROJECT_ROOT, 'media', 'WeChat_20250221230915.mp4')
    frames_output_dir = os.path.join(PROJECT_ROOT, 'media', 'output')
    annotated_video_path = os.path.join(PROJECT_ROOT, 'media', 'output', 'annotated_video.mp4')
    
    print("Starting video processing pipeline...")
    
    # Process the video:
    # 1. Extract frames from the video.
    # 2. Run object detection on each frame.
    # 3. Annotate the frames with bounding boxes.
    annotated_frames, fps = process_video(video_path, frames_output_dir)
    print(f"Extracted and annotated {len(annotated_frames)} frames at {fps:.2f} FPS.")
    
    # Reassemble the annotated frames back into a video.
    if reassemble_video(frames_output_dir, annotated_video_path, fps):
        print(f"Annotated video successfully saved as {annotated_video_path}.")
    else:
        print("Failed to reassemble the annotated video.")

if __name__ == '__main__':
    main()
