# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class GameItem(scrapy.Item):
    date = scrapy.Field()
    team_name = scrapy.Field() #wyciagnac wczesniej z url
    opponent_name = scrapy.Field()
    at_home = scrapy.Field() # wyciagnac z @
    game_won = scrapy.Field() #boolean na podstawie tm_pts - opp_pts
    team_points = scrapy.Field()
    opponent_points = scrapy.Field()
    field_goals = scrapy.Field()
    field_goal_attempts = scrapy.Field()
    field_goal_percentage = scrapy.Field()
    three_pointers = scrapy.Field()
    three_point_atempts = scrapy.Field()
    three_point_percentage = scrapy.Field()
    free_throws = scrapy.Field()
    free_throw_attempts = scrapy.Field()
    free_throw_percentage = scrapy.Field()
    offensive_rebounds = scrapy.Field()
    defensive_rebounds = scrapy.Field() # wyliczyc z trb-orb
    total_rebounds = scrapy.Field()
    assists = scrapy.Field()
    steals = scrapy.Field()
    blocks = scrapy.Field()
    turnovers = scrapy.Field()
    personal_fouls = scrapy.Field()







#
class CarItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    nick = scrapy.Field()
