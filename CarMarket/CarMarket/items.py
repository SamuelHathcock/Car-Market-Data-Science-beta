# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarmarketItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    year_make_model = scrapy.Field()
    price = scrapy.Field()
    odometer = scrapy.Field()
    paintcolor = scrapy.Field()
    titlestatus = scrapy.Field()
    
