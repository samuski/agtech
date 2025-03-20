## Files to add:

- `sam_vit_h_4b8939.pth` in main_module/weights directory.
- Contents of `dataset.zip` in datasets directory in project root.
- Install `Yolov5` separately.
  - Note: I just did git clone in main_module directory, it can be cleaned up later as needed.
- Install SAM model. (Maybe not needed? Yolo seems to also have segmentation.)

## Instructions

- Main dashboard and services: `docker-compose up -d --build`
- Segmentation: From Docker exec, cd to `main_module/` and run `python segmentation.py`.
  - This is hardcoded to run on the images in `"raw image pool"/` in `datasets/` directory in root.
- Training: From Docker exec, cd to `main_module/yolov5` and run `python train.py --data "../main_module/dataset/Grape Disease Dataset.v2-grape-disease-dataset-with-leaves.yolov5pytorch/data.yaml" --weights yolov5l.pt --img 640 --batch 16 --epochs 100 --device 0`.
  - Note that the command trains on the grape diseas dataset that's already labeled and assumes there's GPU on device0. Can take some time to finish.

## Considerations

- Using higher model of YOLO is possible. There are YOLOv11 and v12 available.
  - We will need to consider that these models will be heavier and will take more time in training and running them.
  - Then there's the question of can we run the model on the drone itself.

Somehow pass the weights (2GB+)
Somehow pass images in zip.
