# -*- coding: utf-8 -*-
import scrapy
from twisted.internet import reactor, defer
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import datetime

nextCard = ''

class EventSpider(scrapy.Spider):
    name = 'event'
    allowed_domains = ['www.google.com']
    
    eventScript = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(5))

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
            'lua_source': self.eventScript,
            'wait': 5,
        })

    def parse(self, response):
        cardDate = response.xpath("//div[@class='tsp-cpd tsp-rpd tsp-flr']//span[@class='tsp-cp']/text()").get()
        newDate = cardDate.split(",")

        if (newDate[0]=="today" or newDate[0]=="yesterday"):
            nextCard = response.xpath("//a[@tabindex='0']/following-sibling::a[1]/div/span/div/span/span/text()").get()
        else:
            dateObj = datetime.datetime.strptime(cardDate, '%a, %b %d, %I:%M %p')
            if(datetime.datetime.now() - dateObj).total_seconds() > 0:
                print((datetime.datetime.now() - dateObj).total_seconds())
                nextCard = response.xpath("//a[@tabindex='0']/text()").get()

            else:
                print((datetime.datetime.now() - dateObj).total_seconds())
                nextCard = response.xpath("//a[@tabindex='0']/following-sibling::a[1]/div/span/div/span/span/text()").get()

class fighterSpider(scrapy.Spider):
    name = 'event'
    allowed_domains = ['www.tapology.com']

    fighterScript = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(5))
            
            input_box = assert(splash:select("#siteSearch"))
            input_box:focus()
            input_box:send_text(splash.event)
            assert(splash:wait(5))
            
            btn = assert(splash:select("#search"))
            btn:mouse_click()
            assert(splash:wait(5))
            
            splash:set_viewport_full()
            
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.tapology.com", callback=self.parse, endpoint="execute", args={
            'lua_source': self.fighterScript,
            'wait': 5,
            'event': nextCard
        })
    
    def parse(self, response):
        event = response.xpath("//div[@class='searchResultsEvent']/table/tbody/tr[1]/text()").get()
        print(event)
        print("**********************************************")

configure_logging()
runnerOne = CrawlerRunner()
runnerTwo = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runnerOne.crawl(EventSpider)
    yield runnerTwo.crawl(fighterSpider)
    reactor.stop()

crawl()
reactor.run()

