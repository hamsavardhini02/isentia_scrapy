from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from isentia_scrapy.items import IsentiaScrapyItem


class GuardianSpider(CrawlSpider):
    name = "g_news"
    allowed_domains = ["theguardian.com"]
    start_urls = [
        "https://www.theguardian.com/international"
    ]
    # crawling should scrap with in the domain 'theguardian.com'
    rules = (
        Rule(LinkExtractor(allow="theguardian.com"), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        self.log("Scraping: " + response.url)

        for article in response.css('div.fc-item__content'):
            item = IsentiaScrapyItem()
            item["headline"] = article.css('span.js-headline-text').extract_first()
            item["url"] = article.css('a::attr("href")').extract_first()
            item['text'] = article.css('div.fc-item__content > div.fc-item__standfirst').extract_first()
            item["article_about"] = article.css('span.fc-item__kicker').extract_first()
            item["comment_count"] = article.xpath(
                '//aside > a[@class ="fc-trail__count fc-trail__count--commentcount"]/text()').extract_first()
            yield item
