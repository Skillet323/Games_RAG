#settings.py
BOT_NAME = 'fandom_parser'
SPIDER_MODULES = ['fandom_parser.spiders']
NEWSPIDER_MODULE = 'fandom_parser.spiders'

ITEM_PIPELINES = {
    'fandom_parser.pipelines.CVAnalysisPipeline': 100,
}

# Конфиги
CHUNK_SIZE = 700  

IMAGES_STORE = None