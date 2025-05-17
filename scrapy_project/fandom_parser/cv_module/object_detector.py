# object_detector.py
from PIL import Image
from typing import List
from ultralytics import YOLO
import tempfile
import os

model = YOLO('yolov8n.pt')

def detect_objects(image_path: str) -> List[dict]:
    results = model(image_path)
    dets = []
    for det in results[0].boxes.data.tolist():
        x1, y1, x2, y2, conf, cls_idx = det
        label = results[0].names[int(cls_idx)]
        bbox = [x1, y1, x2 - x1, y2 - y1]
        dets.append({'label': label, 'bbox': bbox, 'confidence': float(conf)})
    return dets


def detect_objects_pil(image: Image.Image) -> List[dict]:

    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    try:
        tmp_file.close()
        image.save(tmp_file.name, format="JPEG")
        return detect_objects(tmp_file.name)
    finally:
        try:
            os.remove(tmp_file.name)
        except Exception:
            pass