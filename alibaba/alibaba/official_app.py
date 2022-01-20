import requests
from scrapy import Selector


def splitter(raw_text, headings, count):
    item_ = dict()
    text_list = raw_text.split(headings[count].strip())
    bulk_text = text_list[-1]
    item_['Heading'] = headings[count - 1].strip()
    item_['Description'] = text_list[0].strip()
    return bulk_text, item_


if __name__ == '__main__':
    url = 'https://ourkindofcrazy.com/blog/would-you-rather-questions-for-couples/'
    r = requests.get(url)
    response = Selector(text=r.text)

    heads = response.css('#main h2 ::text').getall()

    all_text = response.css('div[class="entry-content clear"] ::text').getall()
    joined_text = ' '.join(all_text)

    item = dict()

    remaining_text_list = joined_text.split(heads[0].strip())
    joined_text = remaining_text_list[-1]

    for index in range(1, len(heads)):
        joined_text, item = splitter(joined_text, heads, index)
        print(item)

    remaining_text_list = joined_text.split('Share with your friends!')
    item['Heading'] = heads[-1].strip()
    item['Description'] = remaining_text_list[0].strip()
    print(item)
