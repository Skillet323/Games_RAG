# fandom_parser/cv_module/object_detector.py
from PIL import Image
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8x.pt')

CELESTE_CLASSES = {
    0: "person",  # Madeline
    43: "strawberry",  # Red Strawberry
    44: "strawberry",  # Golden Strawberry
    45: "platform",  # Moving Platform
    46: "hazard",  # Spike
    47: "heart",  # Crystal Heart
    48: "gate",  # Heart Gate
    49: "cassette",  # Cassette Tape
    50: "cloud",  # Cloud Platform
    51: "zipper",  # Zipper
    52: "moon",  # Moon Berry
    53: "car",  # Intro Car
    54: "bird",  # The Bird
    55: "mountain",  # Celeste Mountain
    56: "tree",  # Tree
    57: "rock",  # Rock
    58: "sign",  # Signpost
    59: "door",  # Door
    60: "lamp",  # Lamp
    61: "window",  # Window
    62: "building",  # Building
    63: "bridge",  # Bridge
    64: "ladder",  # Ladder
    65: "rope",  # Rope
    66: "flag",  # Flag
    67: "banner",  # Banner
    68: "statue",  # Statue
    69: "monument",  # Monument
    70: "fence",  # Fence
    71: "bench",  # Bench
    72: "table",  # Table
    73: "chair",  # Chair
    74: "bed",  # Bed
    75: "shelf",  # Shelf
    76: "cabinet",  # Cabinet
    77: "drawer",  # Drawer
    78: "stool",  # Stool
    79: "ramp",  # Ramp
    80: "slope",  # Slope
    81: "ladder",  # Ladder
    82: "pole",  # Pole
    83: "pipe",  # Pipe
    84: "wire",  # Wire
    85: "cable",  # Cable
    86: "rope",  # Rope
    87: "chain",  # Chain
    88: "string",  # String
    89: "thread",  # Thread
    90: "vine",  # Vine
    91: "branch",  # Branch
    92: "leaf",  # Leaf
    93: "flower",  # Flower
    94: "bush",  # Bush
    95: "grass",  # Grass
    96: "moss",  # Moss
    97: "fungus",  # Fungus
    98: "lichen",  # Lichen
    99: "alga",  # Alga
    100: "seaweed",  # Seaweed
}

def detect_objects_pil(image: Image.Image) -> list:
    try:
        results = model(image)
        detections = []
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf)
                cls_id = int(box.cls)
                
                # Фильтр по порогу уверенности
                if conf >= 0.6 and cls_id in CELESTE_CLASSES:
                    detections.append({
                        "label": CELESTE_CLASSES[cls_id],
                        "bbox": [x1, y1, x2 - x1, y2 - y1],
                        "confidence": conf
                    })
        return detections
    except Exception as e:
        logger.error(f"Ошибка детекции объектов: {e}")
        return []