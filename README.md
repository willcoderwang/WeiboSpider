# WeiboSpider

Just a practice of using [Scrapy](https://scrapy.org).

### Usage

Make sure you have scrapy installed.

```
  $ git clone https://github.com/willcoderwang/WeiboSpider.git
  $ cd WeiboSpider
  $ scrapy crawl weibo
```

You may want to save the results, use the following command instead. It will save the results in a file, one result per line in json.

```
  $ scrapy crawl weibo -o results.jl
```
