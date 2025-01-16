import scrapy


class BayutSpider(scrapy.Spider):
    name = "bayut"
    allowed_domains = ["www.bayut.com"]
    start_urls = ["https://www.bayut.com/to-rent/property/dubai/"]

    def parse(self, response):
        pass
