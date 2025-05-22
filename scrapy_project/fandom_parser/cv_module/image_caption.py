# fandom_parser/cv_module/image_caption.py
from transformers import pipeline
from PIL import Image
import torch

#Salesforce/blip2-opt-2.7b - 16 гигов
#Salesforce/blip-image-captioning-large - 2 гб
image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

def generate_caption_pil(image: Image.Image) -> str:
    try:
        result = image_to_text(image, max_new_tokens=64)
        return result[0]['generated_text'].strip()
    except Exception as e:
        print(f"Ошибка генерации описания: {e}")
        return ""