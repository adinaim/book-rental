import scrapy
from parser.items import QuoteItem   


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = 'https://quotes.toscrape.com/'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        quote_item = QuoteItem()
        for quote in response.css('div.quote'):
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import random

from slugify import slugify

class BookSpider(CrawlSpider):   # scrapy.Spider
    name = 'mybook'
    start_urls = ['https://mybook.ru/']

    def __init__(self):
        self.data = []
        rules = (
        Rule(LinkExtractor(allow='catalog/books')),
        Rule(LinkExtractor(allow='author'), callback='parse_books')
        )
        list_of_books = rules
        self.data.extend(list_of_books)

    def parse_books(self, response):

        author = response.css('div.dey4wx-1.jVKkXg::text').get().replace('&nbsp;', ' ')
        title = response.css('h1.sc-bdfBwQ.lnjchu-0.jzwvLi.gUKDCi.sc-1c0xbiw-11.bzVsYa::text').get().replace('&nbsp;', ' ')
        slug = slugify(title)
        image_link = response.xpath('//div/picture/source/@srcset').get().split(',')[0]    
        description = response.css('div.iszfik-2.gAFRve p::text').get() 
        genre = response.css('div.sc-1sg8rha-0.gHinNz div a::text').extract()      

        book = {slug:  
            {
            'author': author,
            'title': title,
            'image': image_link,
            'description': description,
            'genre': genre,
            'number_of_copies': random.randint(1, 10) 
            }
        }

        return book