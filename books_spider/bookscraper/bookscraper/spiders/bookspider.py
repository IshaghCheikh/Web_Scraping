import scrapy
from bookscraper.items import bookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            
            relative_url = book.xpath('h3/a/@href').get()
            if 'catalogue' in relative_url:
                book_page_url = 'https://books.toscrape.com/' + relative_url 
            else:
                book_page_url =   'https://books.toscrape.com/catalogue/' +  relative_url 
            yield response.follow(book_page_url , callback = self.parse2)
            
        next_page = response.xpath('//li[@class = "next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)    
              
    def parse2(self , response):
        book_item = bookItem()
        book_item['title'] = response.xpath('//div[@class = "col-sm-6 product_main"]/h1/text()').get()
        book_item['price'] =  response.xpath('//div[@class = "col-sm-6 product_main"]/p[@class = "price_color"]/text()').get()
        book_item['description'] =  response.xpath('//div[@class = "sub-header"]/following-sibling::p/text()').get()
        book_item['category']  =  response.xpath('//ul[@class = "breadcrumb"]/li[@class = "active"]/preceding-sibling::li[1]/a/text()').get()
        yield book_item
            
        