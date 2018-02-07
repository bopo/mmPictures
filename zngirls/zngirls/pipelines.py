# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request

class ZngirlsPipeline(object):
    def process_item(self, item, spider):
        return item

class ZngirlsImagePipeline(ImagesPipeline):

    default_headers = {
        'referer': 'http://www.nvshens.com/rank/sum/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, headers=self.default_headers, dont_filter=True)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        
        if not image_paths:
            raise DropItem("Item contains no images")
        
        item['image_paths'] = image_paths
        
        return item            