# tasks.py
from celery import shared_task
from video_processing import process_video, reassemble_video
import os

@shared_task
def process_video_task(video_path, frames_output_dir, annotated_video_path):
    annotated_frames, fps = process_video(video_path, frames_output_dir)
    success = reassemble_video(frames_output_dir, annotated_video_path, fps)
    return {
        "frames": annotated_frames,
        "fps": fps,
        "video_reassembled": success
    }
