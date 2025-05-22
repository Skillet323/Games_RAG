# fandom_parser/settings.py
BOT_NAME = 'fandom_parser'

SPIDER_MODULES = ['fandom_parser.spiders']
NEWSPIDER_MODULE = 'fandom_parser.spiders'

ITEM_PIPELINES = {
    'fandom_parser.pipelines.CVAnalysisPipeline': 100,
}
CHUNK_SIZE = 700  
TOKENIZER_MODEL = 'gpt2'

YOLO_MODEL_PATH = 'yolov8x.pt'

DOWNLOAD_TIMEOUT = 15
RETRY_TIMES = 3