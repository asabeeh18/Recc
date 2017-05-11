from __future__ import print_function

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    url0 = 'https://myanimelist.net/anime/'
    # url1 = '/Cowboy_Bebop/stats&m=all#members'
    animeCount = 34815

    def start_requests(self):
        global animeCount
        global url0
        for i in range(animeCount):
            yield scrapy.Request(url=(url0+i), callback=self.parse)

    def parse(self, response):
        f=open("opFIle", 'w', 1024);


        next_page = response.css('.table-recently-updated+div a::attr("href")').extract()
        if len(next_page)>1:
            next_page=next_page[1]
        else:
            next_page=next_page[0]

        print("~~next page: "+next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
