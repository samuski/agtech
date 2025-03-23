## Requirements

- Ample storage space.
- Patience.

## Files to add:

- Place `best.pt` and [Optional]`sam_vit_h_4b8939.pth` in `weights/` in project root directory.
- [Optional] Contents of `Raw image pool.zip` in a folder named after itself in `datasets/` directory.
- [Optional] Contents of `Grape Disease Dataset.v2-grape-disease-dataset-with-leaves.yolov5pytorch` in a folder named after itself in `dataset/` directory.
- Install `Yolov5` separately.
  - From project root directory, run `git clone https://github.com/ultralytics/yolov5.git`
  - Note: I just did git clone in main_module directory, it can be cleaned up later as needed.
- Install SAM model. (Maybe not needed? Yolo seems to also have segmentation.)

## Instructions

- Main dashboard and services: `docker-compose up -d --build`
  - Debug Note: On Windows, if getting `exec /app/entrypoint.sh: no such file or directory` in container log, this is due to .sh formatting. Switch from CRLF to LF.
- Segmentation: From Docker exec, cd to `main_module/` and run `python segmentation.py`.
  - This is hardcoded to run on the images in `"raw image pool"/` in `datasets/` directory in root.
- Training: From Docker exec, cd to `main_module/yolov5` and run the train command.
  - ex. `python train.py --data "../datasets/Grape Disease Dataset.v2 cleaned/data.yaml" --weights yolov5l.pt --img 1024 --batch 8 --epochs 100 --device 0 --patience 20`.
    - `--data` : path to the `data.yaml` file that will have info on the dataset.
    - `--weights` : weight to train upon.
    - `--img` : the image size, such as 640, 1280, etc. Note that larger image size will require more VRAM.
    - `--batch` : batch size.
    - `--epochs` : how many epochs to run. Too little will cause insufficiently trained weight and too much will cause overmatch on the training dataset.
    - `--device` : GPU device id to train with. If without GPU, omit.
    - `--patience` : how many epochs without improvement of the training before it stops early.
  - Note that the command trains on the `Grape Disease Dataset.v2 cleaned` that's already labeled but strippe of all but leaf labels.

## Considerations

- Using higher model of YOLO is possible. There are YOLOv11 and v12 available.
  - We will need to consider that these models will be heavier and will take more time in training and running them.
  - Then there's the question of can we run the model on the drone itself.

## Data sources

- Should be added later.
