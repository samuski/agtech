import os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UploadForm
from .models import Upload
from main_module.detectors.video_processor import process_video
from main_module.detectors.leaf_detector import get_leaf_detector
import cv2
# For image testing, you could use a similar detection function from detectors/leaf_detector.py

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_instance = form.save()  # saves file to media/uploads/
            # Process the file (for simplicity, assume it's an image; for video, process frame by frame)
            input_file_path = upload_instance.file.path
            
            # Define output directories and file paths
            output_dir = os.path.join(settings.MEDIA_ROOT, 'results')
            os.makedirs(output_dir, exist_ok=True)
            # For demonstration, assume we're processing an image using our detection function

            detector = get_leaf_detector('./weights/best.pt')  # default YOLOv5s if blank

            if is_image(input_file_path):
                image = cv2.imread(input_file_path)
                detections = detector.detect(image)
                # Draw detections on the image
                for det in detections:
                    x, y, w, h = det['bbox']
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2)
                    label = f"{det['label']} {det['confidence']:.2f}"
                    cv2.putText(image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                
                # Save result image
                result_path = os.path.join(output_dir, f"result_{upload_instance.id}.jpg")
                cv2.imwrite(result_path, image)
            elif is_video(input_file_path):
                frames_dir = os.path.join(output_dir, f"frames_{upload_instance.id}")
                os.makedirs(frames_dir, exist_ok=True)
                result_path = os.path.join(output_dir, f"result_{upload_instance.id}.gif")

                process_video(input_file_path, frames_dir, detector, result_path)

                # Save the gif path
                upload_instance.result_file.name = os.path.relpath(result_path, settings.MEDIA_ROOT)
            else:
                # unknown file type
                return render(request, 'dashboard/upload.html', {'form': form, 'error': 'Unsupported file type'})

            # Update model instance
            upload_instance.result_file.name = os.path.relpath(result_path, settings.MEDIA_ROOT)
            upload_instance.processed = True
            upload_instance.save()
            
            return redirect('dashboard:upload_success', upload_id=upload_instance.id)
    else:
        form = UploadForm()
    return render(request, 'dashboard/upload.html', {'form': form})

def upload_success(request, upload_id):
    from .models import Upload
    upload = Upload.objects.get(id=upload_id)
    return render(request, 'dashboard/upload_success.html', {'upload': upload})

import mimetypes

def is_image(file_path):
    mimetype, _ = mimetypes.guess_type(file_path)
    return mimetype and mimetype.startswith('image')

def is_video(file_path):
    mimetype, _ = mimetypes.guess_type(file_path)
    return mimetype and mimetype.startswith('video')
