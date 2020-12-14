# -*- coding: utf-8 -*-
import scrapy
from twisted.internet import reactor, defer
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import datetime

#global nextCard

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
                self.nextCard = response.xpath("//a[@aria-selected='true']/div/span/div/span/span/text()").get()
                print("OPTION A")
                print(self.nextCard)

            else:
                print((datetime.datetime.now() - dateObj).total_seconds())
                self.nextCard = response.xpath("//a[@tabindex='0']/following-sibling::a[1]/div/span/div/span/span/text()").get()
                print("OPTION B")
                print(self.nextCard)
        print(self.nextCard)

class fighterSpider(scrapy.Spider):
    name = 'fighter'
    allowed_domains = ['www.tapology.com']

    fighterScript = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(3))
            
            input_box = assert(splash:select("#siteSearch"))
            input_box:focus()
            input_box:send_text(splash.event)
            assert(splash:wait(3))
            
            btn = assert(splash:select("#search"))
            btn:mouse_click()
            assert(splash:wait(3))
            
            splash:set_viewport_full()
            
            return splash:html()
        end
    '''

    def start_requests(self):
        print(EventSpider.nextCard)
        print("HERE WE ARE!!!!!!!!!!!!!!!!!!!!!!")
        yield SplashRequest(url="https://www.tapology.com", callback=self.parse, endpoint="execute", args={
            'lua_source': self.fighterScript,
            'wait': 5,
            'event': EventSpider.nextCard
        })
    
    def parse(self, response):
        event = response.xpath("//div[@class='searchResultsEvent']/table/tbody/tr[1]/text()").get()
        print(event)
        print("**********************************************")

configure_logging()
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(EventSpider)
    yield runner.crawl(fighterSpider)
    reactor.stop()

crawl()
reactor.run()

