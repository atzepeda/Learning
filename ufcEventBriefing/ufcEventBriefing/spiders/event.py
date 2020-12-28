# -*- coding: utf-8 -*-
import scrapy
import globals
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerRunner
import datetime


class EventSpider(scrapy.Spider):
    name = 'event'
    allowed_domains = ['www.google.com']
    nextCard = ''
    
    eventScript = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(3))
            input_box = assert(splash:select(".gLFyf.gsfi"))
            input_box:focus()
            input_box:send_text("ufc")
            assert(splash:wait(3))
            btn = assert(splash:select(".gNO89b"))
            btn:mouse_click()
            assert(splash:wait(3))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    def start_requests(self):
        print("EVERYTHING IS GOING ACCORDING TO PLAN")
        yield SplashRequest(url="https://www.google.com", callback=self.parse, endpoint="execute", args={
            'lua_source': self.eventScript,
        })

    def parse(self, response):
        print("HAVE WE MADE IT YET!?!?!?!?!?!")
        cardDate = response.xpath("//div[@class='tsp-cpd tsp-rpd tsp-flr']//span[@class='tsp-cp']/text()").get()
        newDate = cardDate.split(",")

        if (newDate[0]=="today" or newDate[0]=="yesterday"):
            self.nextCard = response.xpath("//a[@tabindex='0']/following-sibling::a[1]/div/span/div/span/span/text()").get()
        else:
            dateObj = datetime.datetime.strptime(cardDate, '%a, %b %d, %I:%M %p')
            if(datetime.datetime.now() - dateObj).total_seconds() > 0:
                print((datetime.datetime.now() - dateObj).total_seconds())
                #self.nextCard = response.xpath("//a[@aria-selected='true']/div/span/div/span/span/text()").get()
                self.nextCard = response.xpath("//a[@tabindex='0']/following-sibling::a[1]/div/span/div/span/span/text()").get()
                print("OPTION A")
                print(self.nextCard)
                globals.q.put(self.nextCard)

            else:
                print((datetime.datetime.now() - dateObj).total_seconds())
                #self.nextCard = response.xpath("//a[@tabindex='0']/following-sibling::a[1]/div/span/div/span/span/text()").get()
                self.nextCard = response.xpath("//a[@aria-selected='true']/div/span/div/span/span/text()").get()
                print("OPTION B")
                print(self.nextCard)
                globals.q.put(self.nextCard)
        print(self.nextCard)

