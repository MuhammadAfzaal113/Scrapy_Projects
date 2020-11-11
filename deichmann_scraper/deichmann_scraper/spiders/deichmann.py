import json
from scrapy import Spider, Request, Selector


class DeichmannSpider(Spider):
    name = 'deichmann'
    start_urls = ['https://www.deichmann.com/GB/en/shop/welcome.html']
    base_url = 'https://www.deichmann.com/'
    api_url = "https://www.deichmann.com/GB/en/shop/ws/restapi/v1/product/{}?prop=sizeVariants"

    headers = {
        'Accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
    }

    def parse(self, response):
        for link in response.css("mega-dropdown div a::attr(href)")[:-3].extract():
            yield Request(url=self.base_url + link, callback=self.products)

    def products(self, response):
        landing_page = response.css("#landingPage_teaser div div a::attr(href)").get()

        if landing_page:
            yield Request(url=self.base_url + landing_page, callback=self.products)
        else:
            products = response.css(".product-item a::attr(href)").extract()
            next_page = response.css(".PAGINGUP::attr(href)").get()

            for product in products:
                yield Request(url=self.base_url + product, callback=self.product_page)

            if next_page:
                yield Request(url=self.base_url + next_page, callback=self.products)

    def product_page(self, response):
        url = response.url
        product_id = url.split('/')[-2]
        url = self.api_url.format(product_id)

        yield Request(url=url,
                      callback=self.scrape_data,
                      meta={"resp": response.body}
                      )

    def scrape_data(self, response):
        resp = response.meta["resp"]
        resp = Selector(text=resp)
        body = json.loads(response.body)
        vars = body['variants']

        for var in vars:
            size = dict()
            size['size'] = var['size']['value']
            size['sizingSystemName'] = var['size']['sizingSystemName']
            size['color_name'] = var['color']['name']
            size['Available'] = var['available']

            item = dict()
            item['name'] = resp.css(".product-name::text").get()
            item["price"] = resp.css("span[itemprop='price']::text").get()
            item['item_no'] = resp.css(".article-code::text").get().replace("\xa0", "")
            item['size'] = size

            yield item
