# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose, Identity


def unicode_to_ascii(str):
    return str.encode('ascii', errors='ignore')

def feet_to_centimeters(feet, inches):
    return int(round(2.54*inches + 30.48*feet))

def pounds_to_kilograms(pounds):
    return int(round(0.4536*int(pounds)))


def feet_to_inches(feet, inches):
    return feet*12 + inches

def extract_height(str):
    feet = int(str.split('-')[0])
    inches = int(str.split('-')[1])
    return feet_to_inches(feet, inches)

def extract_height_si(str):
    feet = int(str.split('-')[0])
    inches = int(str.split('-')[1])
    return feet_to_centimeters(feet, inches)

def is_left_handed(str):
    if 'left' in str.lower():
        return True
    return False

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
    attendance = scrapy.Field()



class PlayerLoader(ItemLoader):
    default_input_processor = MapCompose(unicode.strip, unicode_to_ascii)
    default_output_processor = TakeFirst()

    # height_in = Compose(strip, unicode_to_ascii)
    height_out = Compose(TakeFirst(), extract_height)
    height_si_out = Compose(TakeFirst(), extract_height_si)
    weight_out = Compose(TakeFirst(), int)
    weight_si_out = Compose(TakeFirst(), pounds_to_kilograms)
    left_handed_out = Compose(TakeFirst(), is_left_handed)

class PlayerItem(scrapy.Item):
    height = scrapy.Field()
    height_si = scrapy.Field()
    weight = scrapy.Field()
    weight_si = scrapy.Field()
    left_handed = scrapy.Field()



class TeamLoader(ItemLoader):
    pass

class TeamItem(scrapy.Item):
    championships = scrapy.Field()
    full_name = scrapy.Field()
    playoff_appearances = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    seasons = scrapy.Field()



class SeasonItem(scrapy.Item):
    coaches = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    attendance = scrapy.Field()
    games = scrapy.Field()



#
class CarItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    nick = scrapy.Field()
