# -*- coding: utf-8 -*-
import scrapy
import re


class CarsSpider(scrapy.Spider):

    name = "buscar"
    allowed_domains = ["rj.olx.com.br"]
    start_urls = ['https://rj.olx.com.br/rio-de-janeiro-e-regiao/servicos']

    def parse(self, response):
        items = response.xpath(
            '//ul[@id="main-ad-list"]/li[not(contains(@class, "list_native"))]'
        )

        for item in items:
            url = item.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)
        next_page = response.xpath(
            '//div[contains(@class, "module_pagination")]//a[@rel = "next"]/@href'
        )
        if next_page:
            self.log('Próxima Página: {}'.format(next_page.extract_first()))
            # self.log('Próxima Página: %s' % next_page.extract_first())
            yield scrapy.Request(
                url=next_page.extract_first(), callback=self.parse
            )
   
    def parse_detail(self, response):
        titulo = response.xpath('//title/text()').extract_first()
        descricao = response.xpath("//meta[@name='description']/@content")[0].extract()
        telefones=re.findall(r'\b\(?\d{2}\)?\s\d\s\d{4}\s\d{4}\b|\b\(?\d{3}\)?-\d{5}-\d{4}\b|\b\d{11}\b|\b\(?\d{2}\)?\s\d\d{4}-\d{4}\b|\b\(?\d{2}\)?-\d{5}-\d{4}\b|\b\(?\d{2}\)?\d{5}-\d{4}\b|\b\(?\d{2}\)?\s\d\d{4}\d{4}\b|\b\(?\d{2}\)?\s\d\.\d{4}-\d{4}\b|\b\(?\d{2}\)?\s\d\d{4}\s\d{4}\b|\b\(?\d{2}\)\d{5}\d{4}\b|\b\(?\d{2}\)\d{5}-\d{4}\b|\b\d{12}\b|\b\(?\d{2}\)?\s\d\s\d{4}-\d{4}\b|\b\d{2}\s\d{5}\s\d{2}\s\d{2}\b|\b\d{2}-\s\d{9}\b|\b\d{3}\s\d{9}\b|\b\d{3}\s\d\s\d{4}-\d{4}\b',descricao)
	
	print(telefones) 
	d=len(telefones)
	a=telefones
	c=0
	while c<d:
	   a[c] = '55'+re.sub(r'[^0-9]+', '', telefones[c])
	   print(a)
	   c= c+1

	
        yield {
	    
            'titulo': titulo,
            'descricao': descricao,
            'telefones': telefones,
	    'a': a,
            
        }

	 

