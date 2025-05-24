from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from fandom_parser.items import CelestePageItem

class CelesteSpider(CrawlSpider):
    name = "celeste_ink"
    allowed_domains = ["celeste.ink"]  # Обновлено
    start_urls = ["https://celeste.ink/wiki/Main_Page"]  # Основная страница

    rules = [
        Rule(
            LinkExtractor(
                allow=r"/wiki/[^:]+$",
                deny=[r"\.(?:png|jpg|jpeg|gif|svg)$", r"\?diff=", r"\?oldid="],
                deny_domains=["static.wikitide.net"]  # Домен изображений
            ),
            callback="parse_page",
            follow=True
        )
    ]

    def parse_page(self, response):
        item = CelestePageItem()
        item['doc_id'] = response.url.split('/')[-1]

        # Заголовок
        title = response.css('h1#firstHeading span.mw-page-title-main::text').get(default='').strip()
        item['title'] = title

        item['url'] = response.url
        
        # Категории (в MediaWiki они обычно внизу страницы)
        item['categories'] = response.css('.catlinks ul li a::text').getall()
        
        # Дата последнего изменения
        item['last_modified'] = response.css('#footer-info-lastmod::text').get(default='').strip()
        
        # Извлечение текста
        item['full_text'] = self.extract_full_text(response)

        # Изображения и подписи
        image_elements = response.css('div.mw-parser-output img')
        item['image_urls'] = image_elements.css('::attr(src)').getall()
        
        # Подписи к изображениям (в MediaWiki — .thumbcaption, figcaption)
        item['image_captions'] = [
            caption.strip() for caption in 
            response.css('div.mw-parser-output .thumbcaption::text, '
                        'div.mw-parser-output figcaption::text').getall()
        ]

        return item

    def extract_full_text(self, response):
        blocks = response.css('div.mw-parser-output > *')
        texts = []
        for b in blocks:
            tag = b.root.tag
            if tag in ['h2', 'h3', 'h4']:
                sec = b.css('span.mw-headline::text').get()
                if sec:
                    texts.append(f"## {sec}")
            elif tag == 'p':
                txt = ' '.join(b.css('::text').getall()).strip()
                if txt:
                    texts.append(txt)
            elif tag in ['ul', 'ol']:
                for li in b.css('li'):
                    li_txt = ' '.join(li.css('::text').getall()).strip()
                    if li_txt:
                        texts.append(f"- {li_txt}")
        return '\n'.join(texts)