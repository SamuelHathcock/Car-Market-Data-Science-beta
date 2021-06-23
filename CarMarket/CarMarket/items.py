# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader

from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

def removeFluff(value: str):
    return value.replace('\n', '')

class CarmarketItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor = TakeFirst())
    year_make_model = scrapy.Field(input_processor=MapCompose(removeFluff), output_processor = TakeFirst())
    price = scrapy.Field(output_processor = TakeFirst())
    odometer = scrapy.Field(output_processor = TakeFirst())
    paintcolor = scrapy.Field(output_processor = TakeFirst())
    titlestatus = scrapy.Field(output_processor = TakeFirst())
    
        # input_processor = MapCompose(remove_tags),
        # output_processor = TakeFirst()