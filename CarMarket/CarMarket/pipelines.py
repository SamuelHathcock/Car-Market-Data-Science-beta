# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class CarmarketPipeline:

    def __init__(self):
        self.create_conn()
        self.create_table()
    
    def create_conn(self):
        self.conn = sqlite3.connect("test.db")
        self.curr = self.conn.cursor()
    
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS cars_sqlite""")
        self.curr.execute("""create table cars_sqlite (
            title text,
            price text,
            odometer text
        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        print("Pipelines = " + item['title'] + " " + item['price'] )
        return item

    def store_db(self, item):
        self.curr.execute("""INSERT into cars_sqlite values(?,?,?)""",(
            item['title'],
            item['price'],
            item['odometer']
        ))
        self.conn.commit()




