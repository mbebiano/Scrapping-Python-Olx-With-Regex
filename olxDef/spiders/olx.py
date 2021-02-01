# -*- coding: utf-8 -*-
import scrapy
import re


class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['sp.olx.com.br']
    start_urls = ['https://sp.olx.com.br/sao-paulo-e-regiao/servicos?sct=10&sct=9&sct=6&sct=2&sct=4&sct=5&sct=11&sf=1']

    def parse(self, response):
        items = response.xpath(
            '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[14]/ul/li/a'
        )
        for item in items:
            url = item.xpath('./@href').extract_first()
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//*[@id="column-main-content"]/div[18]/div/div[1]/div/a[@data-lurker-detail="next_page"]/@href'
        )
        if next_page:
            self.log('Próxima Página: {}'.format(next_page.extract_first()))
            yield scrapy.Request(
                url=next_page.extract_first(), callback=self.parse
            )

    def parse_detail(self, response):
        title = response.xpath('/html/head/meta[@property="og:description"]').extract_first()
        links = response.xpath('./@href').extract_first()
        telefones = re.findall(
            r'\b\(?\d{2}\)?\s\d\s\d{4}\s\d{4}\b|\b\(?\d{3}\)?-\d{5}-\d{4}\b|\b\d{11}\b|\b\(?\d{2}\)?\s\d\d{4}-\d{4}\b|\b\(?\d{2}\)?-\d{5}-\d{4}\b|\b\(?\d{2}\)?\d{5}-\d{4}\b|\b\(?\d{2}\)?\s\d\d{4}\d{4}\b|\b\(?\d{2}\)?\s\d\.\d{4}-\d{4}\b|\b\(?\d{2}\)?\s\d\d{4}\s\d{4}\b|\b\(?\d{2}\)\d{5}\d{4}\b|\b\(?\d{2}\)\d{5}-\d{4}\b|\b\d{12}\b|\b\(?\d{2}\)?\s\d\s\d{4}-\d{4}\b|\b\d{2}\s\d{5}\s\d{2}\s\d{2}\b|\b\d{2}-\s\d{9}\b|\b\d{3}\s\d{9}\b|\b\d{3}\s\d\s\d{4}-\d{4}\b',
            title)

        print(telefones)
        d = len(telefones)
        a = telefones
        c = 0
        while c < d:
            a[c] = '+55' + str(re.sub(r'[^0-9]+', '', telefones[c]))
            print(a)
            c = c + 1        

        yield {
            'title': title,
            'telefones': telefones,
            'links': links,
        }


