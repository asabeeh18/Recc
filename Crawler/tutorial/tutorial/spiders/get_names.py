from __future__ import print_function

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://myanimelist.net/anime/1/Cowboy_Bebop/stats&m=all#members',
    ]

    def parse(self, response):
        print ("---HERE RESPONSE")
        print (response)
        print ("---HERE END RESPONSE")
        #for quote in response.css('td.borderClass.di-t.w100 > div.di-tc.va-m.al.pl4'):
        for quote in response.css('.di-tc.va-m.al.pl4>a::text'):
            print("Looping")
            print("-----::"+str(quote.extract()))
        print ("---HERE END OUTPUT")
