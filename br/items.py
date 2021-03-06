# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
# from datetime import date
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose, Identity


def unicode_to_ascii(s):
    return s.encode('ascii', errors='ignore')


def feet_to_centimeters(feet, inches):
    return int(round(2.54*inches + 30.48*feet))


def pounds_to_kilograms(pounds):
    return int(round(0.4536*int(pounds)))


def feet_to_inches(feet, inches):
    return feet*12 + inches


def extract_height(s):
    feet = int(s.split('-')[0])
    inches = int(s.split('-')[1])
    return feet_to_inches(feet, inches)


def extract_height_si(s):
    feet = int(s.split('-')[0])
    inches = int(s.split('-')[1])
    return feet_to_centimeters(feet, inches)


def is_left_handed(s):
    if 'left' in s.lower():
        return True
    return False


def get_wins(s):
    return int(s.split('-')[0])


def get_losses(s):
    return int(s.split('-')[1].strip(','))


def get_full_name(s):
    return s.split(',')[0].strip()


def get_attendance(s):
    try:
        attendance = int(s.split()[0].replace(',', ''))
    except:
        attendance = None
    return attendance


def get_date_from_str(s):
    year = int(s.split('-')[0])
    month = int(s.split('-')[1])
    day = int(s.split('-')[2])
    return datetime.date(year, month, day)


def is_at_home(s):
    print "\t\t\t", s
    if '@' in s:
        s = False
    else:
        s = True
    return s


def game_was_won(s):
    if 'w' in s.lower():
        return True
    return False


def percentage_to_float(s):
    return float('0' + s)*100


def get_season_year(s):
    return int(s.split('/')[-1].split('.')[0])


def get_player_side_id(s):
    return s.split('/')[-1].split('.')[0]


class GameLoader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = Compose(TakeFirst(), int)
    date_out = Compose(TakeFirst(), get_date_from_str)
    opponent_name_out = Compose(TakeFirst())
    game_won_out = Compose(TakeFirst(), game_was_won)
    field_goal_percentage_out = Compose(TakeFirst(), percentage_to_float)
    free_throw_percentage_out = Compose(TakeFirst(), percentage_to_float)
    three_point_percentage_out = Compose(TakeFirst(), percentage_to_float)


class GameItem(scrapy.Item):
    date = scrapy.Field()
    team_name = scrapy.Field()  # wyciagnac wczesniej z url
    opponent_name = scrapy.Field()
    at_home = scrapy.Field()  # wyciagnac z @
    game_won = scrapy.Field()  # boolean na podstawie tm_pts - opp_pts
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
    defensive_rebounds = scrapy.Field()  # wyliczyc z trb-orb
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
    site_id_out = Compose(TakeFirst(), get_player_side_id)


class PlayerItem(scrapy.Item):
    height = scrapy.Field()
    height_si = scrapy.Field()
    weight = scrapy.Field()
    weight_si = scrapy.Field()
    left_handed = scrapy.Field()
    site_id = scrapy.Field()


class TeamLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = Identity()
    championships_out = Compose(TakeFirst(), int)
    playoff_appearances_out = Compose(TakeFirst(), int)
    wins_out = Compose(TakeFirst(), unicode.split, TakeFirst(), get_wins)
    losses_out = Compose(TakeFirst(), unicode.split, TakeFirst(), get_losses)
    full_name_out = Compose(TakeFirst(), get_full_name)


class TeamItem(scrapy.Item):
    championships = scrapy.Field()
    full_name = scrapy.Field()
    playoff_appearances = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    seasons = scrapy.Field()


class SeasonLoader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = Identity()

    attendance_out = Compose(TakeFirst(), unicode.strip, get_attendance)
    wins_out = Compose(TakeFirst(), unicode.split, TakeFirst(), get_wins)
    losses_out = Compose(TakeFirst(), unicode.split, TakeFirst(), get_losses)
    year_out = Compose(TakeFirst(), get_season_year)


class SeasonItem(scrapy.Item):
    coaches = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    attendance = scrapy.Field()
    games = scrapy.Field()
    year = scrapy.Field()


class CarItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    nick = scrapy.Field()
