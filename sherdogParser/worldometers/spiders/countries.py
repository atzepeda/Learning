# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.sherdog.com']
    start_urls = ['https://www.sherdog.com/fighter/Ovince-St-Preux-38842']

    def parse(self, response):
        title = response.xpath("//h2/text()").get()
        countries = response.xpath("//td/a/text()").getall()

        yield {
            'title': title,
            'countries': countries
        }
