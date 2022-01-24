from scrapy import Spider, Request
from datetime import datetime

main_category = 'Leather Remnants'


class SearchSpider(Spider):
    name = 'search'
    start_urls = [
    ]

    done = [
        'https://www.leatherhidestore.com/leather-for-upholstery',
        'https://www.leatherhidestore.com/auto-upholstery-leather-interior',
        'https://www.leatherhidestore.com/suede-leather.html',
        'https://www.leatherhidestore.com/embossed-leather-croc-embossed/croc-embossed.html',
        'https://www.leatherhidestore.com/embossed-leather-croc-embossed.html',
        'https://www.leatherhidestore.com/embossed-leather-croc-embossed/hornback.html',
        'https://www.leatherhidestore.com/closeouts.html'
        'https://www.leatherhidestore.com/shop-leather-by-color.html',
        'https://www.leatherhidestore.com/leather-remnants-leather-pieces.html',

    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
    }

    today = 'Outputs/output_' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.csv'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        'CONCURRENT_REQUESTS': 12,
        'FEED_EXPORT_FIELDS': [
            'Name', 'Category', 'Sub-Category', 'Price', 'Competitor Price', 'Color', 'Size', 'Stock', 'CARE',
            'Texture', 'Finish',
            'Feel', 'Quality', 'Notes', 'Important Note', 'Images', 'Project Images', 'Product URL'],
        'FEED_URI': today,
        'FEED_FORMAT': 'csv'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, headers=self.headers, callback=self.special)

    def parse(self, response):
        cats = response.css('.category_data_uplohold h3 a ::attr(href)').getall()
        if not cats:
            cats = response.css('.category-item-title a ::attr(href)').getall()
        for cat in cats:
            yield Request(url=cat, headers=self.headers, callback=self.sub_cat_parse)

    def special(self, response):
        links = response.css('.remnants_category ul li a ::attr(href)').getall()
        for link in links:
            yield Request(url=link, headers=self.headers, callback=self.sub_cat_parse)

    def sub_cat_parse(self, response):
        print(response)
        sub_cats = response.css('a[class="btn"] ::attr(href)').getall()
        category_title = response.css('.mobile-header-text span[class="botom-title"] ::text').getall()
        if not category_title:
            category_title = response.css('h1 span[data-ui-id="page-title-wrapper"] ::text').getall()
        for sub_cat in sub_cats:
            yield Request(url=sub_cat, callback=self.detail_page, headers=self.headers,
                          meta={'sub_title': ' '.join(category_title)})

    def detail_page(self, response):
        li_items = ['Name: ', 'Color: ', 'Size:', 'Stock:', 'CARE:', 'Notes:', 'Texture:', 'Finish:',
                    'Feel:', 'Quality: ']
        item = dict()
        item['Category'] = main_category
        item['Sub-Category'] = response.meta.get('sub_title').strip()
        for li in response.css('.extra-description ul li'):
            label = li.css('label ::text').get('')
            if label in li_items:
                item[label.split(':')[0]] = li.css('span ::text').get('').strip()
            if label not in li_items:
                print(label, '========', response.url)
        item['Price'] = response.css('.special-price .price ::text').get('').strip()
        old_price = response.css('.copatitor-price.old-price ::text').getall()
        if old_price:
            item['Competitor Price'] = old_price[1].strip()
        imgs = response.css('#MagicToolboxSelectors25981 a ::attr(href)').getall()
        if not imgs:
            imgs = response.css('img[itemprop="image"] ::attr(src)').getall()
        if imgs:
            item['Images'] = ', '.join(imgs)
        note = response.css('.important-note p ::text').getall()
        item['Important Note'] = ' '.join(note)
        project_imgs = response.css('.customer-project-info ul li img ::attr(src)').getall()
        if project_imgs:
            item['Project Images'] = ', '.join(project_imgs)
        item['Product URL'] = response.url

        yield item

        more = response.css('#related-detail-page').get()
        if more:
            more_items = response.css('#related-detail-page ol li a[class="related-product-button"]'
                                      ' ::attr(href)').getall()
            if more_items:
                for url in more_items:
                    yield Request(url=url, headers=self.headers, callback=self.detail_page,
                                  meta={'sub_title': item['Sub-Category']})
