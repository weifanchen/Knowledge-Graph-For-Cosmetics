# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class SephoraItem(scrapy.Item):
    item_type = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    product_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    product_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    brand = scrapy.Field(
        output_processor=TakeFirst()
    )
    loves = scrapy.Field(
        output_processor=TakeFirst()
    )
    reviews = scrapy.Field(
        output_processor=TakeFirst()
    )
    stars = scrapy.Field(
        output_processor=TakeFirst()
    )
    prices = scrapy.Field()
    sizes = scrapy.Field()
    category = scrapy.Field(
        output_processor=TakeFirst()
    )
    subcategory = scrapy.Field(
        output_processor=TakeFirst()
    )
    minicategory = scrapy.Field(
        output_processor=TakeFirst()
    )
    pass

class ReviewItem(scrapy.Item):
    item_type = scrapy.Field(
        output_processor=TakeFirst()
    )
    customer_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    product_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    # description = scrapy.Field(
    #     output_processor=TakeFirst()
    # )
    rating = scrapy.Field(
        output_processor=TakeFirst()
    )
    age = scrapy.Field(
        output_processor=TakeFirst()
    )
    eye_color = scrapy.Field(
        output_processor=TakeFirst()
    )
    hair_color = scrapy.Field(
        output_processor=TakeFirst()
    )
    skin_tone = scrapy.Field(
        output_processor=TakeFirst()
    )
    skin_type = scrapy.Field(
        output_processor=TakeFirst()
    )
    pass
