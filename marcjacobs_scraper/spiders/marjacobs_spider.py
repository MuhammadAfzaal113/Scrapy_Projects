import re
import time

from scrapy import Spider, Request


class MarjacobsSpiderSpider(Spider):
    name = 'jacobs'
    start_urls = ['https://www.marcjacobs.com/']

    headers = {
        'authorit': 'www.marcjacobs.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigat',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__cfduid=d6afea0e91c3d804a06133dd1580848f01601836232; dwanonymous_925c5c911dedc4dc1a345433a8c82587=ab0uIp07vCPECP8K1lyNEPXPW2; _qubitTracker=0by6o8k0i5q-0kfvfxn92-a287zw0; _gcl_au=1.1.483340674.1601836234; _ga=GA1.2.2124952833.1601836233; _gid=GA1.2.1554665134.1601836235; _scid=c5f19369-aa0f-4d2f-b240-11c8b7d0feac; _sctr=1|1601751600000; __cq_uuid=ab0uIp07vCPECP8K1lyNEPXPW2; _hjid=715294f5-e976-4742-b52a-2ffd00f71b47; GlobalE_CT_Data=%7B%22CUID%22%3A%22697689588.278554207.494%22%2C%22CHKCUID%22%3Anull%7D; _pin_unauth=dWlkPVpUY3dPRFUzTVdZdFpXUXlNQzAwTnprNUxXRmlOR0l0TTJGbE1HSXdNRGN6WldJNA; qb_generic=:XT04Z7y:.marcjacobs.com; firsttime_usr=1; __qca=P0-565415411-1601836268613; _fbp=fb.1.1601836269281.1066422826; GlobalE_Welcome_Data=%7B%22showWelcome%22%3Afalse%7D; cqcid=ab0uIp07vCPECP8K1lyNEPXPW2; __cq_dnt=0; dw_dnt=0; __55=%7B%22ms%22%3A%22non-member%22%2C%22st%22%3A%22regular%22%2C%22vF0%22%3A1601836233439%2C%22vF%22%3A%22occasional%22%2C%22vF1%22%3A1601897539318%7D; _hjTLDTest=1; _hjAbsoluteSessionInProgress=0; GlobalE_Full_Redirect=false; emailPopup=true; dwac_1b8b4169444398a5bd71b5531a=ir-kdJjK0qUA6eXedlkE4AaQ66BO3uacA-Q%3D|dw-only|||USD|false|US%2FEastern|true; sid=ir-kdJjK0qUA6eXedlkE4AaQ66BO3uacA-Q; dwsid=SZfCtomWAD1whOyElF2D8sW4jWJfgjQEc4mH7OjjFDL4IwOs0C0L1k2xgobR656oYNRhvj4tKs6NVG1cmsPX4Q==; __cq_bc=%7B%22aaqt-marcjacobs%22%3A%5B%7B%22id%22%3A%22M0016843%22%2C%22sku%22%3A%22191267867335%22%7D%2C%7B%22id%22%3A%22M0015142%22%2C%22sku%22%3A%22191267615080%22%7D%2C%7B%22id%22%3A%22M0015141%22%2C%22sku%22%3A%22191267615882%22%7D%2C%7B%22id%22%3A%22M0016267%22%2C%22sku%22%3A%22191267795300%22%7D%2C%7B%22id%22%3A%22C4003117%22%2C%22sku%22%3A%22191267864808%22%7D%2C%7B%22id%22%3A%22C6000174%22%2C%22sku%22%3A%22191267864907%22%7D%5D%7D; GlobalE_Data=%7B%22countryISO%22%3A%22GB%22%2C%22cultureCode%22%3A%22en-US%22%2C%22currencyCode%22%3A%22GBP%22%2C%22apiVersion%22%3A%222.1.4%22%7D; __kla_id=eyIkcmVmZXJyZXIiOnsidHMiOjE2MDE4MzYyMzUsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vd3d3Lm1hcmNqYWNvYnMuY29tLyJ9LCIkbGFzdF9yZWZlcnJlciI6eyJ0cyI6MTYwMTkyMDI2MSwidmFsdWUiOiIiLCJmaXJzdF9wYWdlIjoiaHR0cHM6Ly93d3cubWFyY2phY29icy5jb20vcGVhbnV0cy14LW1hcmMtamFjb2JzLXRoZS13ZWJiaW5nLXN0cmFwL00wMDE2ODQzLmh0bWw/ZHd2YXJfTTAwMTY4NDNfY29sb3I9NDAxIn19; qb_permanent=0by6o8k0i5q-0kfvfxn92-a287zw0:56:2:5:4:0::0:1:0:BfehTm:Bfe10E:A::::111.119.187.1:lahore:7769:pakistan:PK:31.49:74.4:unknown:unknown:punjab:25878:migrated|1601920261149:ELHa==a=CMdu=MX::XT54102:XT52b4V:0:0:0::0:0:.marcjacobs.com:0; qb_session=2:1:10:ELHa=C:0:XT52b4V:0:0:0:0:.marcjacobs.com; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; _gat__ga=1; _uetsid=b211d550066f11eb9649e7322826948a; _uetvid=b212b840066f11eb87cd01d8c7bece8c'
    }

    cookies = {
        'GlobalE_Data': '%7B%22countryISO%22%3A%22GB%22%2C%22cultureCode%22%3A%22en-US%22%2C%22currencyCode%22%3A%22GBP%22%2C%22apiVersion%22%3A%222.1.4%22%7D'
    }

    def parse(self, response):
        for url in response.css("div.runwayStaticImg__imgCard-media--image a").css("::attr(href)").getall()[1:-1]:
            yield Request(url=url, callback=self.products_page)

    def products_page(self, response):
        for url in response.css('#content a::attr(href)').getall():
            yield response.follow(url=url, callback=self.detail_page, cookies=self.cookies, headers=self.headers)

    def detail_page(self, response):
        item = dict()
        script_data = response.xpath('//*[@id="main"]/script[1]/text()').get()
        data = str(script_data)
        item['Product id'] = self.get_id(data)

        title = response.xpath('//*[@id="main"]/div/section/form/section/div[1]/h2/text()[2]').get()
        if title is None:
            item['Title'] = None
            # item['Title'] = response.css('.toolbar__title ::text').get().replace("\n", '')
        else:
            item['Title'] = title.replace("\n", '')
        # item['Price'] = response.css('.toolbar__price .toolbar__price').css('::text').getall(None)[-1].replace("\n", '')
        item['URL'] = response.url
        counter = 0
        yield item

        while True:
            print(item)
            time.sleep(60)
            counter += 1
            if counter == 2:
                break


    def get_id(self, data):
        id1 = ''.join(re.findall("'C\d*", data))
        if id1 is '':
            id2 = ''.join(re.findall("'M\d*", data))
            return id2
        return id1

