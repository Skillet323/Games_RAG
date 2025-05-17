#cv_runner.py
from .cv_module.image_caption import generate_caption_pil
from .cv_module.object_detector import detect_objects_pil
import requests
from PIL import Image
from io import BytesIO


def analyze_image(image_url: str) -> dict:
    try:
        resp = requests.get(image_url)
        img = Image.open(BytesIO(resp.content)).convert("RGB")
    except Exception as e:
        return {'caption': '', 'objects': [], 'error': str(e)}

    caption = generate_caption_pil(img)
    objects = detect_objects_pil(img)
    return {'caption': caption, 'objects': objects}