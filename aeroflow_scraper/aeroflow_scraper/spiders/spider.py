import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://www.aeroflowperformance.com/']

    def parse(self, response):
        item = dict()
        for level1 in response.css('li.level0'):
            label1 = level1.css('a span::text').get('').strip()
            item['Parent Category'] = label1

            for level2 in level1.css('li.level1'):
                label2 = level2.css('a span::text').get('').strip()
                item['Child Category'] = label2

                for level3 in level2.css('li.level2'):
                    label3 = level3.css('a span::text').get(' ').strip()
                    item['Sub-Child Category'] = label3

                    yield item
