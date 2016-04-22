from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy_blog.items import ScrapyBlogItem
from scrapy.http import Request
class BlogSpider(CrawlSpider):
    name = 'bee'
    allowed_domains = ['segmentfault.com']
    start_urls = ['https://segmentfault.com/blogs?page=']
    # rules = (
    #     Rule(LinkExtractor(allow="page=[0-9]{1,20}"),follow=False,callback='parse_item'),
        # Rule(LinkExtractor(allow="a"),follow=False,callback='parse_post')
    # )
    pageCount = 1;
    def parse(self,response): # parse url
        # title = response.xpath('//h2[@class="title"]/a/text()').extract()
        urls = response.xpath('//h2[@class="title"]/a/@href').extract()
        print(response.url)
        if not urls:
            print("the have not URL!!!")
            yield Request(self.start_urls[0],callback=self.parse_item)
        # else:
        for url in urls:
            newUrl = 'https://segmentfault.com' + url
            # print('===>>>The new URL is :' + newUrl,'count :{0}',len(urls))
            yield Request(newUrl,callback=self.parse_post)

        self.pageCount += 1
        nextPage = self.start_urls[0] + str(self.pageCount)
        yield Request(nextPage,callback=self.parse)
# title : //h1[@id="articleTitle"]/a/text()
# post  : //div[@class="article fmt article__content"]
    def parse_post(self, response):
        title = response.xpath('//h1[@id="articleTitle"]/a/text()').extract()[0]
        article = response.xpath('//div[@class="article fmt article__content"]').extract()[0]
        item = ScrapyBlogItem()
        item['title'] = title
        print(title)
        item['article'] = article
        yield item