# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class CartaCapitalSpider(scrapy.Spider):
    name = 'carta_capital'
    allowed_domains = ['cartacapital.com.br']
    start_urls = []
    visitados = []

    def __init__(self, *a, **kw):
        super(CartaCapitalSpider, self).__init__(*a, **kw)
        with open('seeds/carta_capital.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):

        if (self.responseValida(response) and self.artigoValido(response)):
            yield {
            'titulo': self.getTitulo(response),
            'subtitulo': self.getSubtitulo(response),
            'autor': self.getAutor(response),
            'data': self.getData(response),
            'secao': self.getSecao(response),
            'texto': self.getTexto(response),
            'url': self.getUrl(response),
            }

        for proximaPagina in response.css('a::attr(href)').getall():
            if self.urlValida(proximaPagina):
                self.visitados.append(proximaPagina)
                yield scrapy.Request(proximaPagina, callback=self.parse)

        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def responseValida(self, response):
        return response.css('article').get() is not None

    def artigoValido(self, page_article):
        string_date = page_article.css('div.eltdf-post-info-date a::text').get()
        year = int(string_date.split(" de ")[2])
        return year == 2019

    def urlValida(self, url):
        return ('https://www.cartacapital.com.br/economia' in url or 'https://www.cartacapital.com.br/sociedade' in url or 'https://www.cartacapital.com.br/politica' in url or 'https://www.cartacapital.com.br/justica' in url or 'https://www.cartacapital.com.br/mundo' in url) and (url is not None) and (self.visitados.count(url) == 0)

    def getTitulo(self, response):
        return response.css('h1.eltdf-title-text::text').get()

    def getSubtitulo(self, response):
        return response.css('div.wpb_wrapper h3::text').get()

    def getAutor(self, response):
        return response.css('div.eltdf-title-post-author-info a::text').get()

    def getData(self, response):
        return response.css('div.eltdf-post-info-date a::text').get()

    def getSecao(self, response):
        return response.css('div.eltdf-post-info-category a::text').get()

    def getTexto(self, response):
        # falta ajustar texto
        return response.css('div.eltdf-post-text-inner clearfix p::text, p::text, p::text, p::text, p::text, p::text, p::text').get()

    def getUrl(self, response):
        return response.request.url