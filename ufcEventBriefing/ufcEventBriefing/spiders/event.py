# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import datetime


class EventSpider(scrapy.Spider):
    name = 'event'
    allowed_domains = ['www.google.com']
    
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))

            input_box = assert(splash:select(".gLFyf.gsfi"))
            input_box:focus()
            input_box:send_text("ufc")
            assert(splash:wait(1))

            btn = assert(splash:select(".gNO89b"))
            btn:mouse_click()
            assert(splash:wait(1))

            splash:set_viewport_full()

            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.google.com", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script,
        })

    def parse(self, response):
        cardDate = response.xpath("//div[@class='tsp-cpd tsp-rpd tsp-flr']//span[@class='tsp-cp']/text()").get()
        #print(cardDate.split()[0])
        #print(cardDate)
        newDate = cardDate.split(",")
        #print("*************************************")
        #print(newDate[0])
        if (newDate[0]=="today" or newDate[0]=="yesterday"):
            print("THIS TRIGGERED*******************")
        else:
            dateObj = datetime.datetime.strptime(cardDate, '%a, %b %d, %I:%M %p')
            if(datetime.datetime.now() - dateObj).total_seconds() > 0:
                print("OPTION A")
                yield {
                    'date': dateObj
                }
            else:
                print("OPTION B")
                yield {
                    'date': cardDate
                }

