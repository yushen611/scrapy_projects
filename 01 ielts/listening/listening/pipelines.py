# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ListeningPipeline:

    def open_spider(self,spider):
        print("管道开了")
        self.save_list = []

    def process_item(self, item, spider):
        self.save_list = self.save_list + item["words"]
        return item
    
    def close_spider(self,spider):

        f=open("key.txt","w",encoding="utf-8")
        for line in self.save_list:
            f.write(line+'\n')
            
        f.close()
        print("管道关了,收集的词的个数为{}".format(len(self.save_list)))
        print("管道关了,收集的本子的个数为{}".format(len(self.save_list)/40))
        

