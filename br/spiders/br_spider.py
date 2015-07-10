


import scrapy

from br.items import BrItem

class GamesSpider(scrapy.Spider):
    name = "gamespider"
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
    "http://www.basketball-reference.com/teams/BOS/2010/gamelog"
    ]

    def parse(self, response):
        item = BrItem()
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







'''
/teams/
response.xpath('//*[@id="active"]/tbody//tr[@class="full_table"]/td[1]/a/@href').extract()


/teams/aaa/
response.xpath('//*[@id="ATL"]/tbody//tr/td[1]/a/@href').extract()

zrobic @text()=available

//*[@id="info_box"]/div[4]/ul/li[6]/ul/li[1]/a
'''
