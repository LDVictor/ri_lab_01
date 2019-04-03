# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class CartaCapitalSpider(scrapy.Spider):
    name = 'carta_capital'
    allowed_domains = ['cartacapital.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(CartaCapitalSpider, self).__init__(*a, **kw)
        with open('seeds/carta_capital.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        for article in response.css('div.eltdf-pt-three-item eltdf-post-item eltdf-active-post-page'):
            
            yield {
                'titulo': article.css('div.eltdf-pt-three-content-holder h3 a').get(),
                'subtitulo': article.css('div.eltdf-pt-three-excerpt p').get(),
                'autor': article.css('div.eltdf-post-info-author a').get(),
                'data': article.css('div.eltdf-post-info-date entry-date updated a').get(),
                'secao': 'mundo',
                'texto': article.css('span.text::text').get(),
                'url': article.css('').get()
            }
        #
        # inclua seu código aqui
        #
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        #
        #
        #
