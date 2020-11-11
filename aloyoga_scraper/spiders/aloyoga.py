import json
import scrapy


class AloyogaSpider(scrapy.Spider):
    name = 'aloyoga'
    start_urls = ['https://www.aloyoga.com/']
    api_url = "https://www.aloyoga.com/api/2020-10/graphql.json"

    headers = {
        'x-shopify-storefront-access-token': 'd7ef45a4f583a78079bfebcb868b5931',
        'content-type': 'application/json'
    }

    def parse(self, response):
        for url in response.css('#menSubItem > div > div > ul > li > a ::attr(href)').getall():
            yield response.follow(url=url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        url = response.url
        category = url.split("collections/")
        category = category[1]

        payload = {
            "operationName": "plpProducts",
            "variables": {
                "first": 39,
                "handle": category
            },
            'query': 'query plpProducts($first: Int!, $handle: String!, $after: String, $reverse: Boolean, $sortKey: '
                     'ProductCollectionSortKeys) {collection: collectionByHandle(handle: $handle) '
                     '{ id  products(first: $first, after: $after, sortKey: $sortKey, reverse: $reverse) {      '
                     'pageInfo {        hasNextPage        hasPreviousPage        __typename      }'
                     '      edges {        cursor        node {          ...PlpProductDetails          __typename        }'
                     '        __typename      }     __typename    }    __typename  }'
                     '}fragment PlpProductDetails on Product {  id  images(first: 2, maxWidth: 1) {    edges {      node {'
                     '        originalSrc        __typename      }      __typename    }'
                     '    __typename  }  tags  title  priceRange {    maxVariantPrice {'
                     '      amount      __typename    }    minVariantPrice {     amount      __typename'
                     '   }    __typename  }  availableForSale  handle  availableColors: metafield(namespace: "alo-swatch", key:'
                     ' "available-colors") {   value    __typename } productType  vendor  onlineStoreUrl  __typename}'
        }

        yield scrapy.Request(url=self.api_url,
                             method='POST',
                             headers=self.headers,
                             body=json.dumps(payload),
                             callback=self.content,
                             meta={'url': url}
                             )

    def content(self, response):
        url = response.meta['url']
        body = json.loads(response.text)
        item = dict()
        details = body['data']['collection']['products']['edges']
        for product in details:
            item['id'] = product['node']['id']
            item['title'] = product['node']['title']
            item['maxVariantPrice'] = product['node']['priceRange']['maxVariantPrice']['amount']
            item['minVariantPrice'] = product['node']['priceRange']['minVariantPrice']['amount']
            item['productType'] = product['node']['productType']
            item['vendor'] = product['node']['vendor']
            item['onlineStoreUrl'] = product['node']['onlineStoreUrl']

            yield item

        next_page = body['data']['collection']['products']['pageInfo']['hasNextPage']

        if next_page:
            yield scrapy.Request(url, callback=self.parse_category_page)
