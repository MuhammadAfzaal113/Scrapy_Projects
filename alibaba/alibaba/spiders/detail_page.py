# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import json
from datetime import datetime
import csv


def get_urls_file():
    with open(r'Input/Input URL.csv', 'r') as input_file:
        return [x['URL'] for x in csv.DictReader(input_file)]


class DetailPageSpider(Spider):
    name = 'detail_page'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
    }

    handle_httpstatus_list = [
        400, 401, 402, 403, 404, 405, 406, 407, 409,
        500, 501, 502, 503, 504, 505, 506, 507, 509,
    ]

    today = 'Outputs/output_' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.csv'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
        'CONCURRENT_REQUESTS': 5,
        'FEED_EXPORT_FIELDS': [
            'Product URL', 'Product Title', 'Product Price (left)', 'Name of Supplier', 'Supplier web link',
            'Place of Origin', 'Product Name', 'Single package size', 'Single gross weight', 'Country/Region',
            'Image 1', 'Image 2', 'Image 3', 'Image 4', 'Image 5', 'Image 6', 'Image 7', 'Image 8', 'Image 9',
            'Image 10'
        ],
        'FEED_URI': today,
        'FEED_FORMAT': 'csv'
    }

    def start_requests(self):
        start_urls = get_urls_file()
        for start_url in start_urls:
            yield Request(url=start_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = dict()
        if response.status == 200:
            item['Product URL'] = response.url
            if 'This product is no longer available' in ''.join(response.css('::text').getall()):
                item['Product Title'] = 'Nan'
                item['Product Price (left)'] = 'Nan'
                item['Name of Supplier'] = 'Nan'
                item['Supplier web link'] = 'Nan'
                item['Place of Origin'] = 'Nan'
                item['Product Name'] = 'Nan'
                item['Single package size'] = 'Nan'
                item['Single gross weight'] = 'Nan'
                item['Country/Region'] = 'Nan'
                for index in range(1, 11):
                    item['Image ' + str(index)] = 'Nan'

                yield item
            else:
                item['Product Title'] = response.css('.module-pdp-title ::text').get('Nan')
                item['Product Price (left)'] = response.css('.ma-price-promotion .pre-inquiry-price ::text').get('Nan')
                item['Name of Supplier'] = response.css('.company-name-lite-vb ::text').get('Nan')
                item['Supplier web link'] = response.css('.company-name-lite-vb ::attr(href)').get('Nan')
                item['Images'] = response.css('.main-image-thumb-ul li img[alt="image"] ::attr(src)').getall()
                images = response.css('.image-zoom-container img ::attr(src)').get('Nan')

                if not item['Images']:
                    images = response.css('.image-zoom-container img ::attr(src)').get('Nan')
                    image_list = images.split(',')
                    for index in range(len(image_list)):
                        item['Image ' + str(index+1)] = image_list[index]

                raw_script = ''
                for script in response.css('script'):
                    if 'window.__version__map' in script.css('::text').get(''):
                        raw_script = script.css('::text').get('')
                        break
                raw_script_ = raw_script.strip('''
                      window.__version__map = {
                        'magicEditLoaderVersion': '0.0.75',
                        'icbuPcDetailAll': '0.0.9'
                      }
                      window.detailData =''')
                script = json.loads('{' + raw_script_ + '}}}')
                properties = script.get('globalData').get('product').get('productBasicProperties')
                item['Single package size'] = script.get('globalData').get('trade').get('logisticInfo').get('unitSize')
                item['Single gross weight'] = script.get('globalData').get('trade').get('logisticInfo').get('unitWeight')

                for prop in properties:
                    key = prop.get('attrName')
                    if key == 'Place of Origin':
                        item['Place of Origin'] = prop.get('attrValue') if prop.get('attrValue') else 'Nan'
                        item['Country/Region'] = prop.get('attrValue') if prop.get('attrValue') else 'Nan'

                    elif key == 'Product name':
                        item['Product Name'] = prop.get('attrValue') if prop.get('attrValue') else 'Nan'

                yield item
        else:
            item['Product URL'] = response.url
            item['Product Title'] = 'Nan'
            item['Product Price (left)'] = 'Nan'
            item['Name of Supplier'] = 'Nan'
            item['Supplier web link'] = 'Nan'
            item['Place of Origin'] = 'Nan'
            item['Product Name'] = 'Nan'
            item['Single package size'] = 'Nan'
            item['Single gross weight'] = 'Nan'
            item['Country/Region'] = 'Nan'
            for index in range(1, 11):
                item['Image ' + str(index)] = 'Nan'

            yield item
