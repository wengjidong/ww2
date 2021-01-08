# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CityItem(scrapy.Item):
    # define the fields for your item here like:
    bus_name = scrapy.Field()
    bus_type = scrapy.Field()
    bus_time = scrapy.Field()
    bus_cost = scrapy.Field()
    bus_update = scrapy.Field()
    bus_station = scrapy.Field()
    bus_location = scrapy.Field()
    bus_sequence = scrapy.Field()
    bus_direction = scrapy.Field()
    bus_setop = scrapy.Field()
    bus_polyline = scrapy.Field()
    bus_company = scrapy.Field()



