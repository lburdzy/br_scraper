# -*- coding: utf-8 -*-

import scrapy

from br.items import GameItem, CarItem, PlayerItem, TeamItem, SeasonItem
from br.items import PlayerLoader, TeamLoader, SeasonLoader, GameLoader


# ZROBIC ATTENDANCE w GAMES

class TheUltimateMegaSpiderOfDeath(scrapy.Spider):
    name = 'Ben'
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/teams/"
    ]

    def parse(self, response):
        for sel in response.xpath(
            '//*[@id="active"]/tbody//tr[@class="full_table"]/td[1]/a/@href'
                ).extract():
            team_name = sel.split('/')[2]
            url = response.urljoin(team_name) + '/'
            request = scrapy.Request(url, callback=self.parse_team)
            yield request

    def parse_team(self, response):
        #
        abbr = response.xpath(
            '//*[@id="info_box"]/div[4]/ul/li[1]/a/@href'
                ).extract_first().split('/')[2]
        for sel in response.xpath(
            '//*[@id="' + abbr + '"]/tbody//tr/td[1]/a/@href'
                ).extract():
            url = response.urljoin(sel)[:-5] + '/gamelog/'

            request = scrapy.Request(url, callback=self.parse_season)
            yield request

    def parse_season(self, response):
        # yield {'rty': 'qwerty'}

        for sel in response.xpath(
            ('//table[contains(@id, "tgl_basic")]'
             '/tbody/tr[contains(@id, "tgl_basic")]')
        ):
            item = GameItem()

            # misc data
            item['team_name'] = response.url.split('/')[-4]
            item['date'] = sel.xpath('td[3]/a/text()').extract()
            item['opponent_name'] = sel.xpath('td[5]/a/text()').extract()
            item['at_home'] = sel.xpath('td[4]/text()').extract()
            item['game_won'] = sel.xpath('td[6]/text()').extract()
            item['team_points'] = sel.xpath('td[7]/text()').extract()
            item['opponent_points'] = sel.xpath('td[8]/text()').extract()

            # shooting
            item['field_goals'] = sel.xpath('td[9]/text()').extract()
            item['field_goal_attempts'] = sel.xpath('td[10]/text()').extract()
            item['field_goal_percentage'] = sel.xpath('td[11]/text()').extract()
            item['three_pointers'] = sel.xpath('td[12]/text()').extract()
            item['three_point_atempts'] = sel.xpath('td[13]/text()').extract()
            item['three_point_percentage'] = sel.xpath('td[14]/text()').extract()
            item['free_throws'] = sel.xpath('td[15]/text()').extract()
            item['free_throw_attempts'] = sel.xpath('td[16]/text()').extract()
            item['free_throw_percentage'] = sel.xpath('td[17]/text()').extract()

            # offense
            item['offensive_rebounds'] = sel.xpath('td[18]/text()').extract()
            item['assists'] = sel.xpath('td[20]/text()').extract()
            item['turnovers'] = sel.xpath('td[23]/text()').extract()

            # defence
            item['steals'] = sel.xpath('td[21]/text()').extract()
            item['blocks'] = sel.xpath('td[22]/text()').extract()
            item['personal_fouls'] = sel.xpath('td[24]/text()').extract()

            item['total_rebounds'] = sel.xpath('td[19]/text()').extract()

            yield item


class BRSpider(scrapy.Spider):
    name = 'br'
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/teams/"
    ]

    def parse(self, response):

        for sel in response.xpath(
            '//*[@id="active"]/tbody//tr[@class="full_table"]/td[1]/a/@href'
                ).extract():
            team_name = sel.split('/')[2]
            url = response.urljoin(team_name) + '/'
            request = scrapy.Request(url, callback=self.parse_team)
            yield request

    def parse_team(self, response):
        tl = TeamLoader(item=TeamItem(), response=response)

        playoff_appearances = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[3]/text()'
            ).extract()[0].split('(')[0]  # .strip()
        championships = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[3]/text()'
            ).extract()[1].split('(')[0]
        full_name = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[1]/text()[2]'
            ).extract()  # _first().strip()
        wins = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[2]/text()'
            ).extract()[1].split('(')[0]
        losses = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[2]/text()'
            ).extract()[1].split('(')[0]

        seasons = {}

        tl.add_value('playoff_appearances', playoff_appearances)
        tl.add_value('championships', championships)
        tl.add_value('full_name', full_name)
        tl.add_value('wins', wins)
        tl.add_value('losses', losses)

        abbr = response.xpath(
            '//*[@id="info_box"]/div[4]/ul/li[1]/a/@href'
        ).extract_first().split('/')[2]
        for sel in response.xpath(
            '//*[@id="' + abbr + '"]/tbody//tr/td[1]/a/@href'
        ).extract():
            url = response.urljoin(sel)  # [:-5] + '/gamelog/'

            request = scrapy.Request(url, callback=self.parse_season)
            request.meta['seasons'] = seasons
            print '\n\n\n', request, '\n\n\n'
        tl.add_value('seasons', seasons)
        yield tl.load_item()

    def parse_season(self, response):
        print '\n\n\n', 'qweeeeeeeeeeeeeeee', '\n\n\n'
        sl = SeasonLoader(item=SeasonItem(), response=response)
        seasons = 'qwe'
        print '\n\n\n', seasons, '\n\n\n'
        # seasons_key = response.url
        # print '\n\n\n\n\n', response.url, '\n\n\n\n\n'
        sl.add_value('year', response.url)
        wins = response.xpath(
            '//*[@id="info_box"]/p[2]/text()[1]'
            ).extract_first()  # .strip().replace('-', ',').split(',')[0]
        losses = response.xpath(
            '//*[@id="info_box"]/p[2]/text()[1]'
            ).extract_first()  # .strip().replace('-', ',').split(',')[1]
        attendance = response.xpath(
            '//*[@id="info_box"]/p[4]/text()[2]'
            ).extract_first()  # .split()[0]
        coaches = []
        for coach in response.xpath(
            '//*[@id="info_box"]/p[2]/span[2]/following-sibling::a/text()'
                ).extract():
            coaches.append(coach)

        sl.add_value('wins', wins)
        sl.add_value('losses', losses)
        sl.add_value('attendance', attendance)
        sl.add_value('coaches', coaches)
        seasons['one_season'] = sl.load_item()
        # print sl.load_item()
        # yield sl.load_item()
        yield seasons


class PlayerSpider(scrapy.Spider):
    name = "player"
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/players/g/grekino01.html"
    ]

    def parse(self, response):
        l = PlayerLoader(item=PlayerItem(), response=response)

        height = response.xpath(
            '//p[@class="padding_bottom_half"]/text()'
            ).extract()[2]
        weight = response.xpath(
            '//p[@class="padding_bottom_half"]/text()'
            ).extract()[3].split()[0]
        left_handed = response.xpath(
            '//p[@class="padding_bottom_half"]/text()'
        ).extract()[1]

        l.add_value('height', height)
        l.add_value('height_si', height)
        l.add_value('weight', weight)
        l.add_value('weight_si', weight)
        l.add_value('left_handed', left_handed)
        yield l.load_item()


class GamesSpider(scrapy.Spider):
    name = "game"
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/teams/BOS/2010/gamelog"
    ]

    def parse(self, response):
        xpath = ('//table[contains(@id, "tgl_basic")]'
                 '/tbody/tr[contains(@id, "tgl_basic")]')
        for sel in response.xpath(xpath):
            l = GameLoader(item=GameItem(), response=response)

            date = sel.xpath('td[3]/a/text()').extract()
            opponent_name = sel.xpath('td[5]/a/text()').extract()
            at_home = sel.xpath('td[4]/text()').extract()
            at_home = False if at_home else True
            game_won = sel.xpath('td[6]/text()').extract()
            team_points = sel.xpath('td[7]/text()').extract()
            opponent_points = sel.xpath('td[8]/text()').extract()

            # shooting
            field_goals = sel.xpath('td[9]/text()').extract()
            field_goal_attempts = sel.xpath('td[10]/text()').extract()
            field_goal_percentage = sel.xpath('td[11]/text()').extract()
            three_pointers = sel.xpath('td[12]/text()').extract()
            three_point_atempts = sel.xpath('td[13]/text()').extract()
            three_point_percentage = sel.xpath('td[14]/text()').extract()
            free_throws = sel.xpath('td[15]/text()').extract()
            free_throw_attempts = sel.xpath('td[16]/text()').extract()
            free_throw_percentage = sel.xpath('td[17]/text()').extract()

            # offense
            offensive_rebounds = sel.xpath('td[18]/text()').extract()
            assists = sel.xpath('td[20]/text()').extract()
            turnovers = sel.xpath('td[23]/text()').extract()

            # defence
            steals = sel.xpath('td[21]/text()').extract()
            blocks = sel.xpath('td[22]/text()').extract()
            personal_fouls = sel.xpath('td[24]/text()').extract()

            total_rebounds = sel.xpath('td[19]/text()').extract()

            l.add_value('date',  date)
            l.add_value('opponent_name', opponent_name)
            l.add_value('at_home', at_home)
            l.add_value('game_won', game_won)
            l.add_value('team_points', team_points)
            l.add_value('opponent_points', opponent_points)

            # shooting
            l.add_value('field_goals', field_goals)
            l.add_value('field_goal_attempts', field_goal_attempts)
            l.add_value('field_goal_percentage', field_goal_percentage)
            l.add_value('three_pointers', three_pointers)
            l.add_value('three_point_atempts', three_point_atempts)
            l.add_value('three_point_percentage', three_point_percentage)
            l.add_value('free_throws', free_throws)
            l.add_value('free_throw_attempts', free_throw_attempts)
            l.add_value('free_throw_percentage', free_throw_percentage)

            # offense
            l.add_value('offensive_rebounds', offensive_rebounds)
            l.add_value('assists', assists)
            l.add_value('turnovers', turnovers)

            # defence
            l.add_value('steals', steals)
            l.add_value('blocks', blocks)
            l.add_value('personal_fouls', personal_fouls)

            l.add_value('total_rebounds', total_rebounds)

            yield l.load_item()


class SeasonSpider(scrapy.Spider):
    name = 'season'
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/teams/SAC/2015.html"
    ]

    def parse(self, response):
        season_item = SeasonItem()
        season_item['wins'] = response.xpath(
            '//*[@id="info_box"]/p[2]/text()[1]'
            ).extract_first().strip().replace('-', ',').split(',')[0]
        season_item['losses'] = response.xpath(
            '//*[@id="info_box"]/p[2]/text()[1]'
            ).extract_first().strip().replace('-', ',').split(',')[1]
        season_item['attendance'] = response.xpath(
            '//*[@id="info_box"]/p[4]/text()[2]'
        ).extract_first().split()[0]
        season_item['coaches'] = []
        for coach in response.xpath(
            '//*[@id="info_box"]/p[2]/span[2]/following-sibling::a/text()'
                ).extract():
            season_item['coaches'].append(coach)

        print '\n\n\n', response.url, '\n\n\n'
        url = response.urljoin(response.url)[:-5] + '/gamelog/'
        request = scrapy.Request(url, callback=self.parse_season)
        request.meta['season_item'] = season_item
        yield request
        # yield season_item

    def parse_season(self, response):
        season_item = response.meta['season_item']
        games = season_item['games']
        for sel in response.xpath(
            ('//table[contains(@id, "tgl_basic")]'
             '/tbody/tr[contains(@id, "tgl_basic")]')
                ):
            item = GameItem()

            # misc data
            item['team_name'] = response.url.split('/')[-4]
            item['date'] = sel.xpath('td[3]/a/text()').extract()
            item['opponent_name'] = sel.xpath('td[5]/a/text()').extract()
            item['at_home'] = sel.xpath('td[4]/text()').extract()
            item['game_won'] = sel.xpath('td[6]/text()').extract()
            item['team_points'] = sel.xpath('td[7]/text()').extract()
            item['opponent_points'] = sel.xpath('td[8]/text()').extract()

            # shooting
            item['field_goals'] = sel.xpath('td[9]/text()').extract()
            item['field_goal_attempts'] = sel.xpath('td[10]/text()').extract()
            item['field_goal_percentage'] = sel.xpath('td[11]/text()').extract()
            item['three_pointers'] = sel.xpath('td[12]/text()').extract()
            item['three_point_atempts'] = sel.xpath('td[13]/text()').extract()
            item['three_point_percentage'] = sel.xpath('td[14]/text()').extract()
            item['free_throws'] = sel.xpath('td[15]/text()').extract()
            item['free_throw_attempts'] = sel.xpath('td[16]/text()').extract()
            item['free_throw_percentage'] = sel.xpath('td[17]/text()').extract()

            # offense
            item['offensive_rebounds'] = sel.xpath('td[18]/text()').extract()
            item['assists'] = sel.xpath('td[20]/text()').extract()
            item['turnovers'] = sel.xpath('td[23]/text()').extract()

            # defence
            item['steals'] = sel.xpath('td[21]/text()').extract()
            item['blocks'] = sel.xpath('td[22]/text()').extract()
            item['personal_fouls'] = sel.xpath('td[24]/text()').extract()

            item['total_rebounds'] = sel.xpath('td[19]/text()').extract()

            games[item['date']] = item
        yield season_item


class GamePlayerSpider(scrapy.Spider):
    name = 'gplayer'
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        'http://www.basketball-reference.com/boxscores/201311230SAS.html'
    ]

    def parse(self, response):
        team = 'SAS'
        for sel in response.xpath('//*[@id="' + team +
                                  '_basic"]/tbody/tr[not(@class="no_ranker thead")]'
                                  ):
            # pl = PlayerLoader(item=PlayerItem(), response=response)
            site_id = sel.xpath('td[1]/a/@href').extract_first()

            url = response.urljoin(site_id)

            request = scrapy.Request(url, callback=self.parse_player)
            request.meta['site_id'] = site_id
            yield request

    def parse_player(self, response):
        l = PlayerLoader(item=PlayerItem(), response=response)

        site_id = response.meta['site_id']

        height = response.xpath(
            '//p[@class="padding_bottom_half"]/text()'
            ).extract()[2]
        weight = response.xpath(
            '//p[@class="padding_bottom_half"]/text()'
            ).extract()[3].split()[0]
        left_handed = response.xpath(
            '//p[@class="padding_bottom_half"]/text()'
        ).extract()[1]

        l.add_value('site_id', site_id)
        l.add_value('height', height)
        l.add_value('height_si', height)
        l.add_value('weight', weight)
        l.add_value('weight_si', weight)
        l.add_value('left_handed', left_handed)

        yield l.load_item()

        # yield pl.load_item()


class SeasonSpider2(scrapy.Spider):
    name = 'season2'
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/teams/BOS/"
    ]

    def parse(self, response):
        #
        abbr = response.xpath(
            '//*[@id="info_box"]/div[4]/ul/li[1]/a/@href'
                ).extract_first().split('/')[2]
        for sel in response.xpath(
            '//*[@id="' + abbr + '"]/tbody//tr/td[1]/a/@href'
                ).extract():
            url = response.urljoin(sel)

            request = scrapy.Request(url, callback=self.parse_season)
            yield request

    def parse_season(self, response):
        l = SeasonLoader(item=SeasonItem(), response=response)

        l.add_value('year', response.url)
        wins = response.xpath(
            '//*[@id="info_box"]/p[2]/text()[1]'
            ).extract_first()  # .strip().replace('-', ',').split(',')[0]
        losses = response.xpath(
            '//*[@id="info_box"]/p[2]/text()[1]'
            ).extract_first()  # .strip().replace('-', ',').split(',')[1]
        attendance = response.xpath(
            '//*[@id="info_box"]/p[4]/text()[2]'
            ).extract_first()  # .split()[0]
        coaches = []
        for coach in response.xpath(
            '//*[@id="info_box"]/p[2]/span[2]/following-sibling::a/text()'
                ).extract():
            coaches.append(coach)

        l.add_value('wins', wins)
        l.add_value('losses', losses)
        l.add_value('attendance', attendance)
        l.add_value('coaches', coaches)
        yield l.load_item()


class TeamSpider(scrapy.Spider):
    name = 'team'
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/teams/LAL/"
    ]

    def parse(self, response):
        # team_item = TeamItem()
        l = TeamLoader(item=TeamItem(), response=response)

        playoff_appearances = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[3]/text()'
            ).extract()[0].split('(')[0]  # .strip()
        championships = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[3]/text()'
            ).extract()[1].split('(')[0]
        full_name = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[1]/text()[2]'
            ).extract()  # _first().strip()
        wins = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[2]/text()'
            ).extract()[1].split('(')[0]
        losses = response.xpath(
            '//*[@id="info_box"]/div[5]/div/p[2]/text()'
            ).extract()[1].split('(')[0]

        l.add_value('playoff_appearances', playoff_appearances)
        l.add_value('championships', championships)
        l.add_value('full_name', full_name)
        l.add_value('wins', wins)
        l.add_value('losses', losses)

        yield l.load_item()


class OlxSpider(scrapy.Spider):
    name = 'frank'
    allowed_domains = ['olx.pl']
    start_urls = [
        'http://olx.pl/motoryzacja/samochody/'
    ]

    def parse(self, response):
        item = CarItem()
        for sel in response.xpath(
            '//*[@id="offers_table"]/tbody//tr/td[@class="offer "]'
                ):
            item['price'] = sel.xpath(
                'table/tbody/tr[1]/td[3]/div/p/strong/text()'
                ).extract_first()[:-3]
            item['url'] = sel.xpath(
                'table/tbody/tr[1]/td[2]/div/h3/a/@href'
                ).extract_first()
            # url = item['url']#[0]
            request = scrapy.Request(item['url'], callback=self.parse_car)
            request.meta['item'] = item
            # print 'URL TO: ', url
            yield request

    def parse_car(self, response):
        item = response.meta['item']
        item['title'] = response.xpath(
            '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/h1/text()'
            ).extract_first().strip()
        url = response.xpath('//*[@id="linkUserAds"]/@href').extract_first()
        # print '\nURL TO:\n', url, '\n'
        request = scrapy.Request(url, callback=self.parse_user)
        request.meta['item'] = item
        yield request

    def parse_user(self, response):
        # print '\n\n DZIALA \n\n'
        item = response.meta['item']
        item['nick'] = response.xpath(
            '//*[@id="body-container"]/div/div/div[1]/div/div/h3/text()'
            ).extract_first()
        yield item
