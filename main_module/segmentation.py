import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import torch

from segment_anything import sam_model_registry, SamPredictor

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Using device: {device}")

def mask_to_bbox(mask, image_shape):
    # Get coordinates where mask is True
    y_indices, x_indices = np.where(mask)
    if len(x_indices) == 0 or len(y_indices) == 0:
        return None  # No mask detected
    x_min, x_max = x_indices.min(), x_indices.max()
    y_min, y_max = y_indices.min(), y_indices.max()
    
    # Convert to center-based YOLO format
    img_h, img_w = image_shape[:2]
    x_center = (x_min + x_max) / 2 / img_w
    y_center = (y_min + y_max) / 2 / img_h
    bbox_width = (x_max - x_min) / img_w
    bbox_height = (y_max - y_min) / img_h
    
    return (x_center, y_center, bbox_width, bbox_height)

def prompt(predictor):
    # Define a bounding box that roughly encloses the leaf
    # (x_min, y_min, x_max, y_max)
    input_box = np.array([100, 80, 400, 350])
    # input_box = np.array([50, 50, 450, 400])
    # input_box = np.array([120, 100, 380, 340])
    
    # Define multiple positive points within the leaf area
    input_points = np.array([
        [140, 140],  # Positive point on upper area
        [220, 220],  # Positive point in the center
        [330, 280]   # Positive point near lower-right edge
    ])
    positive_labels = np.ones(len(input_points))  # All positive points (label=1)
    
    # Define negative points to exclude unwanted background regions
    negative_points = np.array([
        [250, 80],
        [100, 350]
    ])

    pred_iou_thresh = 0.75
    stability_score_thresh = 0.80

    multimask_output = True


    positive_labels = np.ones(len(input_points))
    negative_labels = np.zeros(len(negative_points))
    
    # Combine positive and negative points
    all_points = np.concatenate((input_points, negative_points), axis=0)
    all_labels = np.concatenate((positive_labels, negative_labels), axis=0)
    
    print("🤖 Running SAM to generate masks with bounding box and points...")
    
    # Get masks using SAM by including the bounding box
    masks, scores, logits = predictor.predict(
        box=input_box[None, :],
        point_coords=all_points,
        point_labels=all_labels,
        multimask_output=multimask_output,
        # pred_iou_thresh=pred_iou_thresh,
        # stability_score_thresh=stability_score_thresh
    )
    
    print(f"🎯 Generated {len(masks)} mask(s); highest score: {scores[0]:.3f}")
    return masks, scores, logits


# Define your image directory and file extension (e.g., '.jpg')
image_directory = os.path.join(PROJECT_ROOT, 'datasets', 'Raw image pool')
extensions = ['*.jpg', '*.JPEG', '*.png']

image_paths = []
for ext in extensions:
    image_paths.extend(glob.glob(os.path.join(image_directory, ext)))
print(f"📂 Found {len(image_paths)} images.")

# Initialize SAM model
checkpoint_path = os.path.join(PROJECT_ROOT, 'weights', 'sam_vit_h_4b8939.pth')
sam_type = "vit_h"  # or "vit_l", "vit_b"

print("🔄 Loading SAM model...")
sam_model = sam_model_registry[sam_type](checkpoint=checkpoint_path)
sam_model.to(device)
predictor = SamPredictor(sam_model)
print("✅ SAM model loaded and moved to device.")

# Prepare output directory for labels
label_dir = os.path.join(PROJECT_ROOT, 'datasets', 'labels')
os.makedirs(label_dir, exist_ok=True)

# Process each image
for image_path in image_paths:
    print(f"\n🚀 Processing image: {os.path.basename(image_path)}")

    # Load and convert the image
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        print(f"Failed to load {image_path}")
        print(f"❌ Failed to load {image_path}")
        continue
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    print("✅ Image loaded and converted to RGB.")
    
    # Set image for SAM predictor
    predictor.set_image(image_rgb)

    masks, scores, logits = prompt(predictor)

    # Visualize or process the masks (example: show the first mask)
    plt.figure(figsize=(8, 8))
    plt.imshow(image_rgb)
    plt.imshow(masks[0], alpha=0.5)
    plt.title(f"Mask for {os.path.basename(image_path)} (Score: {scores[0]:.3f})")
    plt.axis("off")
    
    # plt.show()

    plt.savefig(os.path.join(label_dir, os.path.basename(image_path).split('.')[0] + '_mask.png'))
    plt.close()

    # Convert mask to bounding box and save label in YOLO format
    bbox = mask_to_bbox(masks[0], image_rgb.shape)
    if bbox:
        # YOLO format: class_id, x_center, y_center, width, height
        label_line = f"0 {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}"
        label_output_path = os.path.join(label_dir, os.path.basename(image_path).split('.')[0] + '.txt')
        with open(label_output_path, 'w') as f:
            f.write(label_line)
        print(f"💾 Label saved to {label_output_path}")
    else:
        print("⚠️ No valid mask found; label not saved.")