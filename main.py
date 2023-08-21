import scrapy
import json

from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from itemadapter import ItemAdapter

class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()

class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()

class QuotesPipeLine:
    authors = []
    quotes = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'fullname' in adapter.keys():
            self.authors.append(
                {
                    'fullname': adapter['fullname'],
                    'born_date': adapter['born_date'],
                    'born_location': adapter['born_location'],
                    'description': adapter['description']
                }
            )

        elif 'tags' in adapter.keys():
            self.quotes.append(
                {
                    'tags': adapter['tags'],
                    'author': adapter['author'],
                    'quote': adapter['quote']
                }
            )

        return


    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as file:
            json.dump(self.quotes, file, ensure_ascii=False, indent=4)
        with open('authors.json', 'w', encoding='utf-8') as file:
            json.dump(self.authors, file, ensure_ascii=False, indent=4)

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {'ITEM_PIPELINES': {QuotesPipeLine: 10}}

    def parse(self, response, **kwargs):
        for quote in response.xpath("/html//div[@class='quote']"):
            q = quote.xpath("span[@class='text']/text()").get()
            author = quote.xpath("span/small/text()").get()
            tags = quote.xpath("div[@class='tags']/a/text()").extract()

            yield QuoteItem(tags=tags, author=author, quote=q)
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(), callback=self.nested_parse)

        next_link = response.xpath("/html//li[@class='next']/a/@href").get()

        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse(self, responce, **kwargs):
        author = responce.xpath("/html//div[@class='author-details']")
        fullname = author.xpath("h3[@class='author-title']/text()").get()
        born_date = author.xpath("p/span[@class='author-born-date']/text()").get()
        born_location = author.xpath("p/span[@class='author-born-location']/text()").get()
        description = author.xpath("div[@class='author-description']/text()").get().strip()

        yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuoteSpider)
    process.start()