# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class IsentiaScrapyItem(scrapy.Item):
    # defining field items for News
    headline = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    article_about = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    text = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    scrape_date = scrapy.Field()
    comment_count = scrapy.Field(default=0)
