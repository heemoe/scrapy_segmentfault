from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy_blog.items import ScrapyBlogItem

class BlogSpider(CrawlSpider):
    name = 'bee'
    allowed_domains = ['segmentfault.com']
    start_urls = ['https://segmentfault.com/blogs?']
    rules = (
        Rule(LinkExtractor(allow="page=[0-9]{1,20}"),follow=True,callback='parse_item'),
    )
    def parse_item(self,response):
        item = ScrapyBlogItem()
        title = response.xpath('//h2[@class="title"]/a/text()').extract()
        url = response.xpath('//h2[@class="title"]/a/@href').extract()
        item_dict = dict(zip(url,title))
        item['page'] = item_dict
        # yield item
        return item

