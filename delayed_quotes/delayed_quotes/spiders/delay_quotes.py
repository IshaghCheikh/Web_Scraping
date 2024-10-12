from typing import Iterable
import scrapy
from scrapy_playwright.page import PageMethod


class DelayQuotesSpider(scrapy.Spider):
    name = "delay_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js-delayed/"]
    def start_requests(self) :
        yield scrapy.Request(
           url = 'https://quotes.toscrape.com/js-delayed/',
           meta = {
               "playwright" : True,
               "playwright_page_methods": [
                    PageMethod('wait_for_selector', '//div[@class = "quote"]',timeout = 100000),
                    PageMethod('wait_for_selector', '//ul[@class = "pager"]',timeout = 100000),
               ]
           }, callback=self.parse
        )
           
        
    

    def parse(self, response):
        quotes = response.xpath('//div[@class = "quote" ]')
        for quote in quotes:
            yield {
                'text' : quote.xpath('.//span[@class = "text"]/text()').get(),
                'author' : quote.xpath('.//small[@class = "author"]/text()').get(),
                'tags' : quote.xpath('.//div[@class = "tags"]/a/text()').extract(),
            }
        next_page = response.xpath('//li[@class = "next"]/a/@href').get()
        if next_page :
            yield scrapy.Request (
                url = "https://quotes.toscrape.com" + next_page,
                meta = {
                    "playwright" : True,
                    "playwright_page_methods": [
                       PageMethod('wait_for_selector', '//div[@class = "quote"]',timeout = 100000),
                       
                       PageMethod('wait_for_selector', '//ul[@class = "pager"]',timeout = 100000),
               
                    ]
                }, callback=self.parse
            )
            
                
            
