#celeste_spider.py
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fandom_parser.items import CelestePageItem
from datetime import datetime

class CelesteSpider(CrawlSpider):
    name = 'celeste'
    allowed_domains = ['celestegame.fandom.com']
    start_urls = ['https://celestegame.fandom.com/wiki/Celeste',
                  "static.wikia.nocookie.net"]

    rules = [
        Rule(LinkExtractor(allow=r'/wiki/', deny=r':'), callback='parse_page', follow=True)
    ]

    def parse_start_url(self, response):
        return self.parse_page(response)

    def parse_page(self, response):
        item = CelestePageItem()
        item['doc_id'] = response.url.split('/')[-1]
        item['title'] = response.css('#firstHeading::text').get(default='').strip()
        item['url'] = response.url
        item['categories'] = response.css('.page-header__categories a::text').getall()
        last_mod = response.css('li#footer-info-lastmod::text').get()
        item['last_modified'] = last_mod.strip() if last_mod else None
        # Контекст раздела
        item['section'] = response.request.meta.get('parent_section', 'root')
        # Сбор структурированного текста
        blocks = response.css('div.mw-parser-output > *')
        md = []
        for block in blocks:
            tag = block.root.tag
            if tag in ['h2','h3','h4']:
                title = block.css('span.mw-headline::text').get()
                if title: md.append(f"## {title}")
            elif tag == 'p':
                txt = ' '.join(block.css('::text').getall()).strip()
                if txt: md.append(txt)
            elif tag in ['ul','ol']:
                for li in block.css('li'):
                    txt = ' '.join(li.css('::text').getall()).strip()
                    if txt: md.append(f"- {txt}")
            elif tag == 'table':
                md.append(block.get())
        item['full_text'] = '\n\n'.join(md)
        item['image_urls'] = response.css('div.mw-parser-output img::attr(src)').getall()
        return item