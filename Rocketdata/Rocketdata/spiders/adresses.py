import scrapy
from Rocketdata import items
from scrapy.selector import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class AdressesSpider(scrapy.Spider):
    name = 'adresses'
    allowed_domains = ['mebelshara.ru/contacts']
    start_urls = ['http://www.mebelshara.ru/contacts/']
    pages_count = 25
    rules = (
            Rule(LinkExtractor(allow=('/page\d+/',)), callback='parse_page'),
        )

    def parse_start_url(self, response):
        return self.parse_page(response)

    def parse(self, response):
        root = Selector(response)
        posts = root.xpath('//div[@class="address.shop-list"]') #'//div[@class="address"]'
        for post in posts:
            item = items.RocketdataItem()
            location = [
                post.xpath('.//div[@class="shop-list.data-shop-latitude "]/text()').extract(),
                post.xpath('.//div[@class="shop-list.data-shop-longitude "]/text()').extract()
            ]
            town_and_adress = [
                post.xpath('.//div[@class="shop-list.js-city "]/text()').extract(),
                post.xpath('.//div[@class="shop-list.shop-address "]/text()').extract()
            ]
            item['address'] = town_and_adress
            item['latlon'] = location
            item['name'] = post.xpath('.//div[@class=" shop-list.shop-name "]/text()').extract()
            item['phones'] = post.xpath('.//div[@class=" shop-list.shop-phone "]/text()').extract()
            item['working_hours'] = post.xpath('.//div[@class=" shop-list.shop-work-time "]/text()').extract()
        return item







