# -*- coding: utf-8 -*-
import scrapy
from zngirls.items import ZngirlsItem

class MmSpider(scrapy.Spider):
    name = 'mm'
    allowed_domains = ['zngirls.com', 'nvshens.com', 'onvshen.com']
    start_urls = ['http://www.nvshens.com/rank/sum/']
    headers = {
        "Referer": "http://www.nvshens.com/rank/sum/",
        "Connection": "keep-alive",
    }

    def parse(self, response):
        pages = response.xpath('//div[@class="pagesYY"]/div/a/@href').extract()
        album = response.xpath('//div[@class="rankli_imgdiv"]/a/@href').extract()
        
        # yield scrapy.Request(response.urljoin(album[0]), headers=self.headers, callback=self.parseItem)
        for item in album:
            url = response.urljoin(item)
            print(url)
            yield scrapy.Request(url, headers=self.headers, callback=self.parseItem)

        for page in pages:
            page = response.urljoin(page)
            print(page)
            yield scrapy.Request(page, headers=self.headers, callback=self.parse)

    def parseItem(self, response):
        pages = response.xpath('//div[@class="igalleryli_div"]/a/@href').extract()
    
        for url in pages:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parsePicture)

    def parsePicture(self, response):
        items = ZngirlsItem()
        pages = response.xpath('//div[@id="pages"]/a/@href').extract()
        photo = response.xpath('//div[@class="gallery_wrapper"]/ul/img/@src').extract()
        title = response.xpath('//div[@class="gallery_wrapper"]/ul/img/@alt').extract()[0]
        
        meta = response.meta
        meta['title'] = title
        
        if not meta.get('image_urls'):
            meta['image_urls'] = []

        meta['image_urls'].extend(photo)

        for i in pages:
            url = response.urljoin(i)
            yield scrapy.Request(url=url, headers=self.headers, meta=meta, callback=self.parsePicture)

        items['image_urls'] = meta['image_urls']
        items['title'] = meta['title']
        yield items


