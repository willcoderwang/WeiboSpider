import scrapy
import json
from urllib import parse as url_parse


class WeiboSpider(scrapy.Spider):
    name = "weibo"

    # lower request frequency to avoid 403
    download_delay = 1

    def __init__(self, start_uid=None, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)

        if start_uid is None:
            self.start_uid = '3655689037'
        else:
            self.start_uid = start_uid

        self.following_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page=1'
        self.mblog_url = 'https://m.weibo.cn/api/container/getIndex?containerid=107603{uid}&page=1'
        self.start_urls = [
            self.following_url.format(uid=self.start_uid),
        ]

    def parse(self, response):
        following_list = json.loads(response.body_as_unicode())
        if following_list['ok'] != 1:
            return

        yield following_list

        next_page_url = self.get_next_page_url(response.url)
        yield scrapy.Request(next_page_url, callback=self.parse)

        for card in following_list['data']['cards'][0]['card_group']:
            followers_count = card['user']['followers_count']
            if followers_count >= 10000:
                uid = card['user']['id']
                yield scrapy.Request(self.mblog_url.format(uid=uid),
                                     callback=self.parse_mblog)

    def parse_mblog(self, response):
        mblog_list = json.loads(response.body_as_unicode())
        if mblog_list['ok'] != 1:
            return

        yield mblog_list

        next_page_url = self.get_next_page_url(response.url)
        yield scrapy.Request(next_page_url, callback=self.parse_mblog)

    @staticmethod
    def get_next_page_url(url):
        u = url_parse.urlparse(url)
        qs = u.query
        pure_url = url.replace('?'+qs, '')
        qs_dict = url_parse.parse_qs(qs)

        page_old = qs_dict.get('page', [1])
        qs_dict['page'] = [str(int(x)+1) for x in page_old]
        new_qs = url_parse.urlencode(qs_dict, doseq=True)

        return pure_url + '?' + new_qs
