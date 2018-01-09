import scrapy
import json
import time


class WeiboSpider(scrapy.Spider):
    name = "weibo"

    def __init__(self, start_uid=None, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)

        if start_uid is None:
            self.start_uid = '3655689037'
        else:
            self.start_uid = start_uid

        self.fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_'
        self.user_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100505'
        self.start_urls = [
            self.fans_url + self.start_uid,
        ]

    def parse(self, response):
        response_dict = json.loads(response.body_as_unicode())
        yield response_dict

        # lower request frequency to avoid 403
        time.sleep(1)

        for fan in response_dict['data']['cards'][0]['card_group']:
            fan_id = fan['user']['id']
            yield scrapy.Request(self.fans_url+str(fan_id),
                                 callback=self.parse)
            yield scrapy.Request(self.user_url+str(fan_id),
                                 callback=self.parse_user)

    def parse_user(self, response):
        yield json.loads(response.body_as_unicode())
