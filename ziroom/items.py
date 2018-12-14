# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiroomItem(scrapy.Item):
    # define the fields for your item here like:

    type = scrapy.Field()
    type_area = scrapy.Field()
    name = scrapy.Field()
    rental = scrapy.Field()#是否首次出租
    area = scrapy.Field()
    floor = scrapy.Field()#几层
    hall = scrapy.Field()#几室几厅
    distance = scrapy.Field()#几室几厅
    subway = scrapy.Field()#地铁
    heating = scrapy.Field()#供暖
    friend_home = scrapy.Field()#友家
    price = scrapy.Field()#价格

