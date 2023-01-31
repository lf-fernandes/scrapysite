import csv
import scrapy
import pandas as pd


class searchitems(scrapy.Spider):
    name = 'search'
    start_urls = [
        'https://www.amazon.com.br/s?rh=n%3A21226688011&fs=true&ref=lp_21226688011_sar'
    ]

    def clean_text(self, text):
        if text:
            text = text.replace('R$ ', 'R$')
        return text

    seen = set()

    def parse(self, response, item=None, nome=None):

        for procurar in response.css('.sg-col-inner'):

            item = {

                'Nome': self.clean_text(procurar.css('.a-text-normal::text').get()),
                'Preço': self.clean_text(procurar.css('.a-offscreen::text').extract_first()),
                'Link': 'https://www.amazon.com.br{}'.format(procurar.css("h2>a::attr(href)").extract_first())

                }

            if item['Nome'] != 'RESULTADOS':

             if item["Link"] and "https://www.amazon.com.brNone" in item["Link"]:
                 item["Link"] = item["Link"].replace("https://www.amazon.com.brNone", "")
             if item["Link"] not in self.seen:
                 self.seen.add(item["Link"])

                 yield item



            prox_pag = response.css('.s-pagination-strip a::attr(href)').getall()
            if prox_pag:
             for link in prox_pag:
              yield response.follow(link, self.parse)
