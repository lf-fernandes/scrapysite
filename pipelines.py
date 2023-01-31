# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#-*- coding: utf-8 -*-

import pandas as pd
import csv
import os

class RaspsitePipeline:
    def process_item(self, item, spider):
        return item


class CsvToExcelPipeline:
        def __init__(self):
            self.csv_file = open('item.csv', 'w', newline='')
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=['Nome', 'Preço', 'Link'])
            self.csv_writer.writeheader()

        def process_item(self, item, spider):
            # escrever dados no arquivo csv
            with open("item.csv", "a", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(item.values())


                # Verifica se o arquivo csv existe antes de ler
            if os.path.exists("item.csv"):
                # ler arquivo csv e converter para xlsx
                df = pd.read_csv("item.csv", encoding='utf-8', header=None, names=["Nome", "Preço", "Link"])
                df.to_excel("item.xlsx", sheet_name="Sheet1", index=False)
            return item



