# fandom_parser/cv_runner.py
from .cv_module.image_caption import generate_caption_pil
from .cv_module.object_detector import detect_objects_pil
import requests
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def analyze_image(image_url: str) -> dict:
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(image_url, headers=headers, timeout=10)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGB")
    except Exception as e:
        logger.error(f"Ошибка загрузки изображения {image_url}: {e}")
        return {'caption': '', 'objects': []}

    try:
        caption = generate_caption_pil(img)
        objects = detect_objects_pil(img)
    except Exception as e:
        logger.error(f"Ошибка анализа изображения {image_url}: {e}")
        return {'caption': '', 'objects': []}

    return {'caption': caption, 'objects': objects}