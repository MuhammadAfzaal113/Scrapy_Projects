# -*- coding: utf-8 -*-
from scrapy import Request, Spider
import json
from datetime import datetime


class SearchSpider(Spider):
    name = 'search'
    start_urls = [
        # 'https://www.macys.com/shop/womens-clothing/womens-coats/Productsperpage/120?id=269',
        'https://www.macys.com/shop/mens-clothing/mens-jackets-coats/Productsperpage/120?id=3763'
                  ]

    base_url = 'https://www.macys.com{}'
    api_url = 'https://www.macys.com/xapi/digital/v1/product/{}'
    image_url = 'https://slimages.macysassets.com/is/image/MCY/products/{}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }
    today = 'Outputs/output_' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.csv'
    custom_settings = {
        # 'DOWNLOAD_DELAY': 0.4,
        'CONCURRENT_REQUESTS': 12,
        'FEED_EXPORT_FIELDS': [
            'Product Name', 'Product URL', 'Brand Name', 'Brand URL', 'Web ID', 'Category', 'Subcategory', 'Rating',
            'Reviews', 'New Price', 'Old Price', 'Regular Offer', 'Colors', 'Size', 'Unit Sale', 'Description', 'Images'
        ],

        'FEED_URI': today,
        'FEED_FORMAT': 'csv'
    }

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(url=start_url, headers=self.headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links = response.css('.productDescription a::attr(href)').getall()

        for link in links:
            yield response.follow(url=link, headers=self.headers, callback=self.detail_page, dont_filter=True)

        next_page = response.css('.next-page a::attr(href)').get('')
        if next_page:
            yield response.follow(url=next_page, headers=self.headers, callback=self.parse)

    def detail_page(self, response):
        item = dict()
        item['Brand Name'] = response.css('.p-brand-title.h4 a[data-auto="product-brand"] ::text').get('').strip()
        brand_url = response.css('.p-brand-title.h4 a[data-auto="product-brand"] ::attr(href)').get('').strip()
        if brand_url:
            item['Brand URL'] = self.base_url.format(brand_url)
        item['Product Name'] = response.css('.p-brand-title.h4 div[data-auto="product-name"] ::text').get('').strip()
        item['Product URL'] = response.url
        web_id = response.css('.c-margin-bottom-4v.web-id.c-legal ::text').get('').strip()
        if web_id:
            item['Web ID'] = web_id.split(': ')[-1]
        else:
            return
        rating = response.css('.p-rev-recmd-csg .black-star ::attr(style)').get('').strip()
        if rating:
            item['Rating'] = rating.split(': ')[-1]
        item['Reviews'] = response.css('.reviews-count ::text').get('').strip()
        item['New Price'] = response.css('.c-red ::text').get('').strip()
        if not item['New Price']:
            item['New Price'] = response.css('.lowest-sale-price .bold ::text').get('').strip()
        item['Old Price'] = response.css('.c-strike ::text').get('').strip()
        item['Regular Offer'] = response.css('.regular-offer-badges .c-link-button ::text').get('').strip()
        colors = response.css('.medium-float-children.color-swatch-collection .color-swatch-div ::attr(aria-label)') \
            .getall()
        item['Colors'] = ', '.join(colors)
        imgs = response.css('.image-grid-container div img[data-name="img"] ::attr(src)').getall()
        sizes = response.css('.swatches-scroller.size-list li ::text').getall()
        size = list()
        for s in sizes:
            size.append(s.strip())
        if size:
            item['Size'] = ', '.join(size)
        else:
            size = response.css('.sc-lbl ::text').getall()
            if size:
                item['Size'] = size[-1].strip()
        item['Unit Sale'] = response.css('.unit-sales strong[data-auto="prod-engage"] ::text').get(' ').strip()
        desc = response.css('.accordion-body ::text').getall()
        description = ''
        for d in desc:
            d = d.strip()
            if d:
                description += d + ' \n'
        item['Description'] = description
        cats = response.css('.breadcrumbs-item ::text').getall()
        try:
            item['Category'] = cats[0].strip()
            item['Subcategory'] = cats[-1].strip()
        except:
            print(response.url, 'Here is the cat problem')

        color_codes = response.css('#color-dropdown-for-sr option ::attr(value)').getall()

        yield Request(url=self.api_url.format(item['Web ID']), callback=self.parse_api, headers=self.headers,
                      meta={'item': item,
                            'color_codes': color_codes,
                            'imgs': imgs})

    def parse_api(self, response):
        item = response.meta.get('item')
        old_imgs = response.meta.get('imgs')
        color_codes = response.meta.get('color_codes')
        api_data = json.loads(response.text)
        product = api_data.get('product')[0]
        colors = product.get('traits').get('colors').get('colorMap')
        image_list = list()
        for code in color_codes:
            image_dict = colors.get(code).get('imagery').get('images')
            for img in image_dict:
                image_list.append(self.image_url.format(img.get('filePath')))
        if image_list:
            item['Images'] = ', '.join(image_list)
        else:
            item['Images'] = ', '.join(old_imgs)

        yield item



# Size:
# https://www.macys.com/shop/product/calvin-klein-jeans-faux-shearling-moto-jacket?ID=13263301&CategoryID=269
#
# Price:
# https://www.macys.com/shop/product/michael-michael-kors-womens-quilted-utility-coat?ID=13065406&CategoryID=269
