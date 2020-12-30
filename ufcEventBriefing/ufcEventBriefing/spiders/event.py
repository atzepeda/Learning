# -*- coding: utf-8 -*-
import scrapy
import globals
import requests
from twisted.internet import reactor, defer
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import datetime


class EventSpider(scrapy.Spider):
    name = 'event'
    allowed_domains = ['www.google.com']
    nextCard = ''
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    
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
            'user-agent': self.USER_AGENT
        })

    def parse(self, response):
        print("HAVE WE MADE IT YET!?!?!?!?!?!")
        cardDate = response.xpath("//div[@class='tsp-cpd tsp-rpd tsp-flr']//span[@class='tsp-cp']/text()").get()
        newDate = cardDate.split(",")

        if (newDate[0]=="today" or newDate[0]=="yesterday"):
            self.nextCard = response.xpath("//a[@tabindex='0']/following-sibling::a[1]/div/span/div/span/span/text()").get()
        else:
            dateObj = datetime.datetime.strptime(cardDate, '%a, %b %d, %I:%M %p')
            #IF: 
            if(datetime.datetime.now() - dateObj).total_seconds() > 0:
                print((datetime.datetime.now() - dateObj).total_seconds())
                self.nextCard = response.xpath("//a[@aria-selected='true']/div/span/div/span/span/text()").get()
                #self.nextCard = response.xpath("//a[@tabindex='0']/following-sibling::a[1]/div/span/div/span/span/text()").get()
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

class fighterSpider(scrapy.Spider):
    name = 'fighter'
    allowed_domains = ['sherdog.com']
    
    BASE_URL = 'https://sherdog.com'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'

    fighterScript = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        assert(splash:go(args.url))
            assert(splash:wait(1))
        
        input_box = assert(splash:select(".search.autocomplete"))
        input_box:focus()
        input_box:send_text(splash.args.event)
        assert(splash:wait(1))
        
        btn = assert(splash:select(".fight_finder > div > div > form > input:nth-child(2)"))
        btn:mouse_click()
        assert(splash:wait(1))
        
        splash:set_viewport_full()
        
        return splash:html()
    end
    '''

    defaultScript = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
        end
    '''

    def start_requests(self):
        event = globals.q.get()
        print(event)
        print("HERE WE ARE!!!!!!!!!!!!!!!!!!!!!!")
        yield SplashRequest(url="https://www.sherdog.com", callback=self.getEventPage, endpoint="execute", args={
            'lua_source': self.fighterScript,
            'event': event,
            'user-agent': self.user_agent
        })

    def getEventPage(self, response):
        event = response.xpath("//div[@class='content table']/table/tbody/tr[2]/td[2]/a/@href").get()
        total_url = self.BASE_URL + event
        print(total_url)
        yield SplashRequest(response.urljoin(event), callback=self.parse, headers={
            'User-Agent': self.user_agent,
            'lua_source': self.defaultScript
        })
    
    def parse(self, response):
        print("ALMOST HAVE IT COMPLETELY RECOMPILED")
        fight_list = []
        fighters = response.xpath("//div[@class='content table']/table/tbody/tr[@class='table_head']/following-sibling::node()[@class='even' or @class='odd']")
        for fighter in fighters:
            fighterOne = fighter.xpath(".//td[2]/div/a[starts-with(@href, '/fighter/')]/span/text()").get()
            fighterTwo = fighter.xpath(".//td[4]/div/a[starts-with(@href, '/fighter/')]/span/text()").get()
            fight = {
                'fighterOne': fighterOne,
                'fighterTwo': fighterTwo
            }
            fight_list.append(fight)
        #print(fight_list)
        globals.q.put(fight_list)

class statsSpider(scrapy.Spider):
    name = 'stats'
    allowed_domains = ['ufcstats.com']
    list_of_fights = []
    
    BASE_URL = 'http://ufcstats.com'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'

    firstStatScript = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(1))
            
            input_box = assert(splash:select(".b-statistics__search-field"))
            input_box:focus()
            input_box:send_text(splash.args.lastName)
            assert(splash:wait(1))
            
            btn = assert(splash:select(".b-statistics__search-btn"))
            btn:mouse_click()
            assert(splash:wait(1))
            
            splash:set_viewport_full()
                    
            return splash:html()
        end
    '''

    defaultScript = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(1))
            return splash:html()
        end
    '''

    firstName = ""
    fakeLastName = ""

    def start_requests(self):
        list_of_fights = globals.q.get()
        print("WE'RE GOING ALL THE WAY THIS TIME")
        lastName = list_of_fights[0].get('fighterOne').split()[1]
        self.firstName = list_of_fights[0].get('fighterOne').split()[0]
        print(self.firstName)
        print(lastName)
        yield SplashRequest(url="http://ufcstats.com/statistics/fighters", callback=self.retrieve_fighter_page, endpoint="execute", args={
            'lua_source': self.firstStatScript,
            'lastName': lastName,
            'user-agent': self.user_agent
        })

    def retrieve_fighter_page(self, response):
        print("-----------------")
        print(self.firstName)
        print("OH BABY")
        table = response.xpath("//table[@class='b-statistics__table']/tbody/tr")
        for row in table:
            fighterName = row.xpath(".//td/a/text()").get()
            self.fakeLastName = fighterName
            print(fighterName)
            if(fighterName==self.firstName):
                print("WE'VE GOT A MATCH")
                link = row.xpath(".//td/a/@href").get()
                print(link)
                yield SplashRequest(url=link, callback=self.retrieve_fighter_stats, endpoint="execute", args={
                    'lua_source': self.defaultScript,
                    'user-agent': self.user_agent
                })
        yield SplashRequest(url="http://ufcstats.com/fighter-details/82a5152216251682", callback=self.retrieve_fighter_stats, endpoint="execute", args={
                    'lua_source': self.defaultScript,
                    'user-agent': self.user_agent
                })
    
    def retrieve_fighter_stats(self, response):
        print("Are we here?")
        print(self.fakeLastName)
        print(response.xpath("//i[@class='b-list__box-item-title']/text()").get())

configure_logging()
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(EventSpider)
    yield runner.crawl(fighterSpider)
    yield runner.crawl(statsSpider)
    #print(globals.q.get())
    reactor.stop()

crawl()
reactor.run()