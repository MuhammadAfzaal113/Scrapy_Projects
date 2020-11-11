import re

from scrapy import Request, Spider


class EbaySpider(Spider):
    name = 'ebay'
    start_url = 'https://www.ebay.de/usr/{}'

    def start_requests(self):
        list_of_users = self.get_username()
        for username in list_of_users:
            url = self.start_url.format(username)
            yield Request(url=url,
                          callback=self.parse,
                          meta={'username': username})

    def parse(self, response):
        item = dict()
        item['name'] = response.meta['username']
        item['feedback'] = response.css(".usrinfo div .mbg-l a::text")[1].extract()
        item['registered since'] = response.css('.info').css('::text').get()
        review_selector = response.css('#member_info > span:nth-child(3) > span:nth-child(1)').get()
        review = review_selector.split()[4]
        review_number = ''.join(re.findall('\d+', review))
        if review_number is '0':
            item['review'] = 'NO'
        else:
            item['review'] = 'YES'

        sale_item_url = response.css('.soi_lk a').css('::attr(href)').get()
        yield Request(url=sale_item_url,
                      callback=self.sale_item,
                      meta={'item':item})

    def sale_item(self, response):
        item = response.meta['item']
        item['product on sale number'] = response.css('.rcnt').css('::text').get()

        yield item

    def get_username(self):
        username_file = open("username.txt", "r")
        list_of_users = username_file.readlines()
        username_file.close()
        return list_of_users
