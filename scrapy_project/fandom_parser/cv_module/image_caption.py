# image_caption.py
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption_pil(image: Image.Image) -> str:
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs, max_length=64, num_beams=5)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def generate_caption(image_path: str) -> str:
    img = Image.open(image_path).convert("RGB")
    return generate_caption_pil(img)