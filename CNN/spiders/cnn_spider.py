import time
import os
import shutil
import re
import scrapy


def get_last_url_from_file():
    try:
        with open('D:\CNN\lasturl.txt', 'r') as text_file:
            return text_file.readline()

    except FileNotFoundError:
        return None

def write_url_to_file(url):
    with open('D:\CNN\lasturl.txt', mode='w') as file_obj:
        file_obj.write(url)


class CnnSpiderSpider(scrapy.Spider):
    name = 'cnn_spider'
    start_urls = 'http://rss.cnn.com/rss/cnn_latest.rss'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        last_url = get_last_url_from_file()
        post_links = [link for link in response.css('link::text').getall() if 'rss.cnn' in link][::-1]

        # For first time run
        if not last_url:
            return self.send_get_request(post_links.pop(0))

        # First probability
        if last_url and last_url in post_links and last_url != post_links[-1]:
            for index, link in enumerate(post_links):
                if last_url == link:
                    return self.send_get_request(post_links.pop(index+1))

        # 2nd probability
        elif last_url and last_url not in post_links:
            return self.send_get_request(post_links.pop(0))

        # 3rd probability
        elif last_url and last_url == post_links[-1]:
            print("Waiting for 5 miniutes")
            time.sleep(300)
            return scrapy.Request(url=self.start_urls, callback=self.parse, dont_filter=True)

    def send_get_request(self, url_to_scrape):
        return scrapy.Request(url=url_to_scrape, callback=self.parse_crawler, meta={'last_url': url_to_scrape})

    def parse_crawler(self, response):
        item = dict()
        item['title'] = response.css('h1::text').get()
        item['description'] = response.css('.el__leafmedia--sourced-paragraph .speakable').css('::text').getall()
        item['text'] = response.css('#body-text').css('::text').getall()

        # yield item

        with open(r'D:\CNN\title.txt', 'w', encoding='utf-8') as titleFile:
            for char in item['title']:
                titleFile.write(char)

        with open(r'D:\CNN\description.txt', 'w', encoding='utf-8') as desFile:
            for char in item['description']:
                if char != ' (CNN)' or ' (CNN Business)':
                    char = self.clean(char)
                    desFile.write(char)

        with open(r'D:\CNN\text.txt', 'w', encoding='utf-8') as textFile:
            for char in item['text']:
                if char != ' (CNN)':
                    # char = self.clean(char)
                    textFile.write(char)

        dir_path = r'D:\CNN\images_folder\full'
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)

        raw_images_url = response.css('#body-text .media__image--responsive').css('::attr(data-src-large)').getall()
        raw_images_url.append(response.css('.media__image--responsive ').css('::attr(data-src-large)').get())
        # print(raw_images)
        clean_image_url = []

        for image_url in raw_images_url:
            imageurl = str(image_url)
            temp_url = "http:" + imageurl
            clean_image_url.append(temp_url)

        length = len(clean_image_url)
        count = str(length)
        with open('D:\CNN\picturecount.txt', 'w') as picFile:
            picFile.write(count)

        yield {
            'image_urls': clean_image_url
        }

        write_url_to_file(response.meta.get('last_url'))

    def clean(self, char):
        return ' '.join(re.findall('[a-zA-Z]+(?=[^)"}]*$)', char))
