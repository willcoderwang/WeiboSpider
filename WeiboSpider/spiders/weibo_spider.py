import scrapy
import json


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    uid = '3655689037'
    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_'
    user_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100505'
    start_urls = [
        fans_url + uid,
    ]

    def parse(self, response):
        response_dict = json.loads(response.body_as_unicode())
        yield response_dict

        for fan in response_dict['data']['cards'][0]['card_group']:
            fan_id = fan['user']['id']
            yield scrapy.Request(self.fans_url+str(fan_id),
                                 callback=self.parse)
            yield scrapy.Request(self.user_url+str(fan_id),
                                 callback=self.parse_user)

    def parse_user(self, response):
        yield json.loads(response.body_as_unicode())
