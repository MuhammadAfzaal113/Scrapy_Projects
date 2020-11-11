import json
from scrapy import Spider, Request


class InstagramSpider(Spider):
    name = 'instagram'
    start_urls = ['https://www.instagram.com/']
    api_url = 'https://z-p3.www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%2219700668658%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A{}'

    headers = {
        'Host': ' z-p3.www.instagram.com',
        'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': ' */*',
        'Accept-Language': ' en-US,en;q=0.5',
        'Accept-Encoding': ' gzip, deflate, br',
        'X-CSRFToken': ' dDXR6N81URMfYSB80TQjiPG6eSqN2gRW',
        'X-IG-App-ID': ' 936619743392459',
        'X-IG-WWW-Claim': ' hmac.AR00ZcM5vsNbsRwPjmvQZaQIs6hv5ymQIREADq46--sa-8ee',
        'X-Instagram-Zero': ' 1',
        'Origin': ' https://www.instagram.com',
        'Connection': ' keep-alive',
        'Cookie': ' ig_did=1E3B1D9C-DCB5-4E3E-B6F3-C68C775CCB2F; mid=X4GQ4wALAAGwXrkx7dPCPmsfFjNY; ig_nrcb=1; shbid=9268; shbts=1602326971.4258566; csrftoken=dDXR6N81URMfYSB80TQjiPG6eSqN2gRW; ds_user_id=19700668658; sessionid=19700668658%3AMe3eMwPImyJEne%3A24; rur=PRN; urlgen="{\\"111.119.187.56\\": 59257}:1kRHbH:EAmMV-eDL6WoMQ3UfTk_olKADyE"; csrftoken=FwtnQqYts3yCFVwQ8keYtxLKnNrvpSq9; ig_did=FDEFF7F0-8FB4-4EC4-89CD-3A8A4FCB3E4C; mid=X4GZNgALAAH2_mQdyPSbi9HqDd9T; ig_nrcb=1; rur=PRN; ds_user_id=19700668658; urlgen="{\\"111.119.187.56\\": 59257}:1kRHd4:M0zFQ9DaN1632bQzdnonATXZrSA"',
    }

    def start_requests(self):
        yield Request(url=self.start_urls[0],
                      callback=self.parse,
                      meta={'extra': '30%7D'}
                      )

    def parse(self, response):
        extra = response.meta['extra']
        url = self.api_url.format(extra)
        yield Request(url=url,
                      callback=self.followers,
                      method='GET',
                      headers=self.headers
                      )

    def followers(self, response):
        data = json.loads(response.body)
        follower = dict()
        # item['No of Followers'] = data['data']['user']['edge_followed_by']['count']
        self.file_name = data['data']['user']['edge_followed_by']['count']
        detail = data['data']['user']['edge_followed_by']['edges']
        for user in detail:
            follower['ID'] = user['node']['id']
            follower['User name'] = user['node']['username']
            follower['Full name'] = user['node']['full_name']
            follower['Profile pic url'] = user['node']['profile_pic_url']
            yield follower
        next_page = data['data']['user']['edge_followed_by']['page_info']['has_next_page']
        if next_page:
            end_cursor = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
            end_cursor = end_cursor[:-2]
            extra = "30%2C%22after%22%3A%22" + end_cursor + "%3D%3D%22%7D"
            url = self.api_url.format(extra)
            yield Request(url=url,
                          headers=self.headers,
                          callback=self.followers,
                          method='GET'
                          )

