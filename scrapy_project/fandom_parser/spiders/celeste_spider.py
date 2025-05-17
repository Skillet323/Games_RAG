#celeste_spider.py
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from fandom_parser.items import CelestePageItem

class CelesteSpider(CrawlSpider):
    name = "celeste"
    allowed_domains = ["celestegame.fandom.com"]
    start_urls = ["https://celestegame.fandom.com/wiki/Celeste"]

    rules = [
        Rule(
            LinkExtractor(
                allow=r"/wiki/[^:]+$",
                deny_domains=["static.wikia.nocookie.net"],
                deny=r"\.(?:png|jpg|jpeg|gif|svg)$"
            ),
            callback="parse_page",
            follow=True
        )
    ]

    def parse_page(self, response):
        item = CelestePageItem()
        item['doc_id'] = response.url.split('/')[-1]
        # Заголовок: точный выбор всех текстовых узлов h1#firstHeading
        title = ''.join(response.xpath('//h1[@id="firstHeading"]//text()').getall()).strip()
        if not title:
            # fallback на h1.page-header__title
            title = response.css('h1.page-header__title::text').get(default='').strip()
        item['title'] = title
        item['url'] = response.url
        item['categories'] = response.css('.page-header__categories a::text').getall()
        item['last_modified'] = response.css('li#footer-info-lastmod::text').get(default='').strip()
        item['full_text'] = self.extract_full_text(response)
        item['image_urls'] = response.css('div.mw-parser-output img::attr(src)').getall()
        return item

    def extract_full_text(self, response):
        blocks = response.css('div.mw-parser-output > *')
        texts = []
        for b in blocks:
            tag = b.root.tag
            if tag in ['h2','h3','h4']:
                sec = b.css('span.mw-headline::text').get()
                if sec:
                    texts.append(f"## {sec}")
            elif tag == 'p':
                txt = ' '.join(b.css('::text').getall()).strip()
                if txt:
                    texts.append(txt)
            elif tag in ['ul','ol']:
                for li in b.css('li'):
                    li_txt = ' '.join(li.css('::text').getall()).strip()
                    if li_txt:
                        texts.append(f"- {li_txt}")
        return ''.join(texts)