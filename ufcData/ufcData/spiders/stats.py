# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest



class StatsSpider(scrapy.Spider):
    name = 'stats'
    allowed_domains = ['www.google.com']
    #start_urls = ['http://www.google.com/']

    script = '''
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))

            input_box = assert(splash:select(".gLFyf.gsfi"))
            input_box:focus()
            input_box:send_text("ufc")
            assert(splash:wait(5))

            btn = assert(splash:select(".gNO89b"))
            btn:mouse_click()
            assert(splash:wait(5))

            splash:set_viewport_full()

            return splash:html()
        end
    '''
    def start_requests(self):
        yield SplashRequest(url="https://www.google.com", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        date = response.xpath("//div[@class='tsp-cpd tsp-rpd tsp-flr']//span[@class='tsp-cp']/text()").get()
        yield {
            'date': date
        }
