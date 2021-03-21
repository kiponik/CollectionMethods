# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
MONGO_URL = "localhost:27017"
# MONGO_URL = "localhost:27019"

class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client['vacancy']

    def process_item(self, item, spider):
        # if spider.name == 'hhru':
        #     item["salary_max"] = -1
        collection = self.db['vacancies']
        collection.insert_one(item)
        # collection.update_one({item['url']}, item, upsert=True)
        # collection.update_one(item, {"$set": item}, upsert=True)
        # if len(item["salary"]) > 1:
        #     item["salary_max"] = item["salary"][1]
        return item
