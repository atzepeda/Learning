# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'fighters'
    allowed_domains = ['www.sherdog.com']
    start_urls = ['https://www.sherdog.com/fighter/Ovince-St-Preux-38842']

    #fighter_name = ''

    def parse(self, response):
        #title = response.xpath("//div[@class='container']//div[@class='content']//div[@class='col_left']//div[@class='module fight_history']//h2[text()='Fight History - Pro']/following::node()//tr[@class='odd' or @class='even']     ...: Pro']/following::node()//tr[@class='odd' or @class='even']")
        fighters = response.xpath("//div[@class='container']//div[@class='content']//div[@class='col_left']//div[@class='module fight_history']//h2[text()='Fight History - Pro']/following::node()//tr[@class='odd' or @class='even']")
        #countries = response.xpath("//td/a/text()").getall()
        for fighter in fighters:
            name = fighter.xpath(".//a[starts-with(@href,'/fighter/')]/text()").get()
            fighter_name = name
            link = fighter.xpath(".//a[starts-with(@href,'/fighter/')]/@href").get()
            #event = fighter.xpath(".//a[starts-with(@href,'/events/')]/text()").get()

           #absolute_url = response.urljoin(link)
            
            yield response.follow(url=link, callback=self.parse_fighter, meta={'fighter_name': name})
            """
            yield {
                'fighter_name': name,
                'fighter_link': link
            }
            """

    def parse_fighter(self, response):
        name = response.request.meta['fighter_name']
        records = response.xpath("//div[@class='container']//div[@class='module bio_fighter vcard']//div[@class='left_side']")
        for record in records:
            win = record.xpath("//div[@class='bio_graph']//span[@class='counter']/text()").get()
            loss = record.xpath("//div[@class='bio_graph loser']//span[@class='counter']/text()").get()
            yield{
                'name': name,
                'win': win,
                'loss': loss
            }
                
