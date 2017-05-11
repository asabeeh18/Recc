from __future__ import print_function

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://myanimelist.net/anime/1',
    ]

    def parse(self, response):
        f1 = open('./vals', 'w')
        print("---HERE RESPONSE")
        # print(response)
        print("---HERE END RESPONSE")
        # for quote in response.css('td.borderClass.di-t.w100 > div.di-tc.va-m.al.pl4'):
        # for quote in response.css('.di-tc.va-m.al.pl4>a::text'):
        #    print("Looping")
        #    print("-----::"+str(quote.extract()))
        resp = response.css('div.js-scrollfix-bottom')
        #print("CSS: " + str(resp))

        # for quote in response.css('.dark_text::text'):
        for div in resp.css('div'):
            print("Poop Loop", file=f1)
            if len(div.css('.dark_text')) > 0:
                print("Looping")
                # print("-----::"+str(div.extract().encode('utf-8')))
                # print("-----:exp: " + str(div.css('::text').extract()))
                print("RUN ME!!!!")
                print("-----:exp: " + str(div.css('::text').extract()))
                kv = div.css('::text').extract()
                print("RUN ME!!!!")
                print("Type: "+str(type(kv)))
                print("STRkv: " + str(kv))

                for j in kv:
                    s=str(j.encode('utf-8')).strip()
                    if(len(s)>0):
                        #print("kv: " + str(j.encode('utf-8')))
                        print(str(j).strip())
                #for j in div.css('.dark_text::text'):
                for j in div.css('.dark_text::text'):
                    print("Values: "+str(j.extract().encode('utf-8')), file=f1)
                # print("!--!", file=f1)
                #print(":"+response.body.decode(div.encoding))
        print("---HERE END OUTPUT")
        f1.close()
        next_page = response.css('.table-recently-updated+div a::attr("href")').extract()
        if len(next_page) > 1:
            next_page = next_page[1]
        else:
            next_page = next_page[0]

        # print("~~next page: " + next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
