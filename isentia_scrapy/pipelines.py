# -*- coding: utf-8 -*-

# Item pipelines are defined here

from w3lib.html import remove_tags
import pymongo
from datetime import datetime, date
from pymongo.errors import ConnectionFailure
from scrapy.conf import settings
from scrapy import log


class IsentiaScrapyPipeline(object):
    collection_name = 'g_news'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE')
        )

    def open_spider(self, spider):
        # Download from compose and Add ssl certificate file
        self.client = pymongo.MongoClient(self.mongo_uri, ssl_ca_certs="./isentia_scrapy/servercert.crt")
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # few news articles may or may not with headline/text
        item['headline'] = remove_tags(item['headline']) if item['headline'] is not None else 'No headline found'
        item['text'] = remove_tags(item['text']) if item['text'] is not None else 'No text found'
        item['article_about'] = remove_tags(item['article_about']) if item['article_about'] is not None else 'No article title found'
        item['scrape_date'] = datetime.now()

        self.db[self.collection_name].insert(dict(item))
        log.msg("Item wrote to MongoDB database {}, collection {}".format(
            settings['MONGODB_DATABASE'],
            self.collection_name))
        return item
