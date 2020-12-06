# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.sherdog.com']
    start_urls = ['https://www.sherdog.com/fighter/Ovince-St-Preux-38842']

    def parse(self, response):
        #title = response.xpath("//div[@class='container']//div[@class='content']//div[@class='col_left']//div[@class='module fight_history']//h2[text()='Fight History - Pro']/following::node()//tr[@class='odd' or @class='even']     ...: Pro']/following::node()//tr[@class='odd' or @class='even']")
        fighters = response.xpath("//div[@class='container']//div[@class='content']//div[@class='col_left']//div[@class='module fight_history']//h2[text()='Fight History - Pro']/following::node()//tr[@class='odd' or @class='even']")
        #countries = response.xpath("//td/a/text()").getall()
        for fighter in fighters:
            name = fighter.xpath(".//a[starts-with(@href,'/fighter/')]/text()")

        yield {
            'fighter_name': name
        }
