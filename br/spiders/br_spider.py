# -*- coding: utf-8 -*-


import scrapy
from functools import partial
from br.items import GameItem, CarItem

class GamesSpider(scrapy.Spider):
    name = "gamespider"
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
    "http://www.basketball-reference.com/teams/BOS/2010/gamelog"
    ]

    def parse(self, response):
        item = GameItem()
        for sel in response.xpath('//table[contains(@id, "tgl_basic")]/tbody/tr[contains(@id, "tgl_basic")]'):


            #misc data
            item['date'] = sel.xpath('td[3]/a/text()').extract()
            item['opponent_name'] = sel.xpath('td[5]/a/text()').extract()
            item['at_home'] = sel.xpath('td[4]/text()').extract()
            item['game_won'] = sel.xpath('td[6]/text()').extract()
            item['team_points'] = sel.xpath('td[7]/text()').extract()
            item['opponent_points'] = sel.xpath('td[8]/text()').extract()

            #shooting
            item['field_goals'] = sel.xpath('td[9]/text()').extract()
            item['field_goal_attempts'] = sel.xpath('td[10]/text()').extract()
            item['field_goal_percentage'] = sel.xpath('td[11]/text()').extract()
            item['three_pointers'] = sel.xpath('td[12]/text()').extract()
            item['three_point_atempts'] = sel.xpath('td[13]/text()').extract()
            item['three_point_percentage'] = sel.xpath('td[14]/text()').extract()
            item['free_throws'] = sel.xpath('td[15]/text()').extract()
            item['free_throw_attempts'] = sel.xpath('td[16]/text()').extract()
            item['free_throw_percentage'] = sel.xpath('td[17]/text()').extract()

            #offense
            item['offensive_rebounds'] = sel.xpath('td[18]/text()').extract()
            item['assists'] = sel.xpath('td[20]/text()').extract()
            item['turnovers'] = sel.xpath('td[23]/text()').extract()



            #defence
            item['steals'] = sel.xpath('td[21]/text()').extract()
            item['blocks'] = sel.xpath('td[22]/text()').extract()
            item['personal_fouls'] = sel.xpath('td[24]/text()').extract()


            item['total_rebounds'] = sel.xpath('td[19]/text()').extract()


            yield item

            # yield scrapy.Request(response.urljoin(url), self)#.parse_titles)




class SeasonSpider(scrapy.Spider):
    name = 'seasonspider'
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
    "http://www.basketball-reference.com/teams/BOS/"
    ]

    def parse(self, response):
        for sel in response.xpath('//*[@id="BOS"]/tbody//tr'):
            qwe = sel.xpath('td[1]/a/@href')
            print qwe



class TeamSpider(scrapy.Spider):
    name = 'teamspider'
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
    "http://www.basketball-reference.com/teams/"
    ]

    def parse(self, response):
        for sel in response.xpath('//*[@id="active"]/tbody//tr[@class="full_table"]'):
            qwe = sel.xpath('td[1]/a/@href').extract()
            print qwe




class TheUltimateMegaSpiderOfDeath(scrapy.Spider):
    name = 'Ben'
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
    "http://www.basketball-reference.com/teams/"
    ]


    def parse(self, response):
        item = GameItem()
        for sel in response.xpath('//*[@id="active"]/tbody//tr[@class="full_table"]/td[1]/a/@href').extract():
            item['team_name'] = sel.split('/')[2]
            #print '\n\nteam_name: \n', item['team_name']
            url = response.urljoin(item['team_name']) + '/'
            request = scrapy.Request(url, callback=self.parse_dir_contents)
            request.meta['item'] = item
            yield request


    def parse_dir_contents(self, response):
        item = response.meta['item']
        #
        #to prawidlowo wyswietla dluga nazwe zespolu:
        item['opponent_name'] = response.xpath('//*[@id="info_box"]/h1/text()').extract()

        print item
        #rty = '//*[@id=' + item['team_name'] + ']/tbody//tr'
        #qwe = response.xpath(rty)
        #print '\n\n RTY:\n', rty
        yield item
        #for sel in response.xpath('//*[@id=' + item['team_name'] + ']/tbody//tr'):
        #    qwe = sel.xpath('td[1]/a/@href')
        #    yield item






class OlxSpider(scrapy.Spider):
    name = 'frank'
    allowed_domains = ['olx.pl']
    start_urls = [
    'http://olx.pl/motoryzacja/samochody/'
    ]


    def parse(self, response):
        item = CarItem()
        for sel in response.xpath('//*[@id="offers_table"]/tbody//tr/td[@class="offer "]'):
            item['price'] = sel.xpath('table/tbody/tr[1]/td[3]/div/p/strong/text()').extract_first()[:-3]
            item['url'] = sel.xpath('table/tbody/tr[1]/td[2]/div/h3/a/@href').extract_first()
            #url = item['url']#[0]
            request = scrapy.Request(item['url'], callback=self.parse_car)
            request.meta['item'] = item
            #print 'URL TO: ', url
            yield request


    def parse_car(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/h1/text()').extract_first().strip()
        url = response.xpath('//*[@id="linkUserAds"]/@href').extract_first()
        #print '\nURL TO:\n', url, '\n'
        request = scrapy.Request(url, callback=self.parse_user)
        request.meta['item'] = item
        yield request


    def parse_user(self, response):
        #print '\n\n DZIALA \n\n'
        item = response.meta['item']
        item['nick'] = response.xpath('//*[@id="body-container"]/div/div/div[1]/div/div/h3/text()').extract_first()
        yield item


'''
/teams/
response.xpath('//*[@id="active"]/tbody//tr[@class="full_table"]/td[1]/a/@href').extract()


/teams/aaa/
response.xpath('//*[@id="ATL"]/tbody//tr/td[1]/a/@href').extract()

zrobic @text()=available

//*[@id="info_box"]/div[4]/ul/li[6]/ul/li[1]/a


//*[@id="BOS"]/tbody/tr[2]/td[1]/a
'''
