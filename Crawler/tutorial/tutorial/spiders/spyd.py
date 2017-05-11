from __future__ import print_function

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://myanimelist.net/anime/1',
    ]

    def parse(self, response):
        print("---HERE RESPONSE")
        print(response)
        print("---HERE END RESPONSE")
        # for quote in response.css('td.borderClass.di-t.w100 > div.di-tc.va-m.al.pl4'):
        # for quote in response.css('.di-tc.va-m.al.pl4>a::text'):
        #    print("Looping")
        #    print("-----::"+str(quote.extract()))
        resp = response.css('td.borderClass')

        print(resp)
        print("---HERE END OUTPUT")
        next_page = response.css('.table-recently-updated+div a::attr("href")').extract()
        if len(next_page) > 1:
            next_page = next_page[1]
        else:
            next_page = next_page[0]

        print("~~next page: " + next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
