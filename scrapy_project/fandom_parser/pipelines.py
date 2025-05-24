# fandom_parser/pipelines.py
from scrapy.utils.project import get_project_settings
from transformers import AutoTokenizer, logging as hf_logging
import logging

hf_logging.set_verbosity_error()
class CVAnalysisPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.chunk_size = settings.get('CHUNK_SIZE', 700)
        self.tok = AutoTokenizer.from_pretrained('gpt2')

    def process_item(self, item, spider):
        # Используем подписи к изображениям из вики вместо CV-анализа пока что
        image_urls = item.get('image_urls', [])
        image_captions = item.get('image_captions', [])
        
        # Сопоставляем URL и подписи
        analyses = []
        for i, url in enumerate(image_urls):
            caption = image_captions[i] if i < len(image_captions) else ""
            analyses.append({
                'caption': caption,
                'objects': []  # Объекты не обнаруживаются
            })
        
        item['cv_analysis'] = analyses

        # Чанкование текста
        text = item.get('full_text', '')
        words = text.split()
        chunks = []
        curr_words = []
        for w in words:
            curr_words.append(w)
            curr_text = ' '.join(curr_words)
            if len(self.tok.encode(curr_text)) > self.chunk_size:
                curr_words.pop()
                chunks.append(' '.join(curr_words))
                curr_words = [w]
        if curr_words:
            chunks.append(' '.join(curr_words))
        item['chunks'] = [{'chunk_id': i, 'text': c} for i, c in enumerate(chunks)]

        return item