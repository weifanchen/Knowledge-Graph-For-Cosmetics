# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
class SephoraPipeline(object):

    def open_spider(self, spider):
        self.productfile = open('sephora_skincare_product.jl', 'w')
        self.reviewfile = open('sephora_skincare_review.jl', 'w')

    def close_spider(self, spider):
        self.productfile.close()
        self.reviewfile.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        if dict(item)['item_type'] == 'product':
            self.productfile.write(line)
        else:
            self.reviewfile.write(line)      
        return item


