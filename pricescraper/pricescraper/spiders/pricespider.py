import scrapy
import json


class PricespiderSpider(scrapy.Spider):
    name = "pricespider"
    
    start_urls = ["https://www.rightmove.co.uk/house-prices/southwark-85215.html?soldIn=1&page=1"]

    def parse(self, response):
        script_content = response.xpath('//script[contains(text(),"window.__PRELOADED_STATE__")]//text()').get()[29:]
        data = json.loads(script_content)
        properties = data['results']['properties']
        for property_item in properties:
            yield {
                'address' : property_item['address'],
                'propertyType' : property_item['propertyType'],
                'transactions' : property_item['transactions'],
                'location' : property_item['location'],
                'url' : property_item['detailUrl']
            }
        
