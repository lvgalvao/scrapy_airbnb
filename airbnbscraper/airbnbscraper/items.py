# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AirbnbscraperItem(scrapy.Item):
    aria_label = scrapy.Field()
    href = scrapy.Field()
    price = scrapy.Field()
    duration = scrapy.Field()
    score = scrapy.Field()
