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

if __name__ == '__main__':
    book = BookSpider()
    print(book)

    # def main(self):
    #     result = []
    #     # for page in range(1, get_last_page(category)+1):
    #     for page in range(1, self.find_last_page()-953):
    #         html = self.get_html(self.HOST, params=f'page={page}', headers=self.HEADERS)
    #         cards = self.get_cards_from_html(html)
    #         list_of_cards = self.parse_from_cards(cards)
    #         result.extend(list_of_cards)
    #     JSonMixin.write_to_db(self, result)





# https://mybook.ru/catalog/books/
# https://mybook.ru/catalog/books/?cursor=cj0xJnA9MS4yNTQ3MzEwMjczNjAyMDA4
# https://mybook.ru/catalog/books/?cursor=cj0xJnA9MS4yMjIxNTcyMTg1NDY0ODI%3D
# https://mybook.ru/author/gabriel-markes/sto-let-odinochestva-1/
# https://mybook.ru/author/aleksandr-dyuma/graf-monte-kristo/


    # def parse(self, response):
    #     for link in response.css(''):
    #         yield response.follow(link, callback=self.parse.book)

    #     for i in range(1, 25):
    #         next_page = f'{self._HOST}/{i}/'
    #         yield response.follow(next_page, callback=self.parse)


        # def get_genres(self):
        #     sel = scrapy.Selector(response)
        #     results = sel.css('div.sc-1sg8rha-0.gHinNz').extract()
        #     for index, result in enumerate(results):
        #         if(index == 1):
        #             print(result) 

        # def get_topics(self):
        #     sel = scrapy.Selector(response)
        #     results = sel.css('div.sc-1sg8rha-0.gHinNz').extract()
        #     for index, result in enumerate(results):
        #         if(index == 1):
        #             print(result)
        



# scrapy crawl 'name' -O 'name.