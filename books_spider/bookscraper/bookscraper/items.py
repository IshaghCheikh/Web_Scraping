# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
def serialize_price(value):
    return float(value.split('£')[1])
def lower_case(value):
    return value.lower()

class bookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field(serializer = serialize_price)
    description = scrapy.Field()
    category = scrapy.Field()
    
