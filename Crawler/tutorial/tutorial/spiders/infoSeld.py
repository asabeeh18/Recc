from __future__ import print_function

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://myanimelist.net/anime/1',
    ]

    def parse(self, response):
        f1 = open('./vals', 'w')
        db = open('./debug', 'w')
        view = open('./vw', 'w')
        tb = open('./tb', 'w')
        #print("---HERE RESPONSE")
        # print(response)
        #print("---HERE END RESPONSE")
        # for quote in response.css('td.borderClass.di-t.w100 > div.di-tc.va-m.al.pl4'):
        # for quote in response.css('.di-tc.va-m.al.pl4>a::text'):
        #    print("Looping")
        #    print("-----::"+str(quote.extract()))
        resp = response.css('div.js-scrollfix-bottom')
        # print("CSS: " + str(resp),file=db)

        # for quote in response.css('.dark_text::text'):
        div = resp.css('div')[0]
        #print(str(div), file=db)
        if len(div.css('.dark_text')) > 0:

            k = []
            for j in div.css('.dark_text::text'):
                print("Values: " + str(j.extract().encode('utf-8')), file=f1)
                s = str(j.extract().encode('utf-8')).strip()
                if (len(s) > 0):
                    k.append(s)
            keys = set(k)
            # print(keys, file=view)

            rawer_list=div.css(':not(h2):not(small):not(script)::text').extract()
            print(rawer_list,file=view)

            raw_list=list()

            for j in rawer_list:
                s = str(j.encode('utf-8')).strip()
                if (len(s) > 0):
                    raw_list.append(s)
            # print(keys, file=db)
            #print(raw_list, file=view)
            table = dict()
            for j in range(0,len(raw_list)):
                s = raw_list[j]
                if len(s) > 0:
                    # print("kv: " + str(j.encode('utf-8')))
                    # print(s, file=f2)
                    if s in keys:
                        v = ""
                        j += 1

                        # print(s + " is in keys", file=db)

                        while raw_list[j][-1] != ':':
                            v += (raw_list[j] + " ")
                            j += 1
                            if j == len(raw_list):
                                break
                        j -= 1
                        print(s+":"+v, file=db)
                        table[s] = v
            for j in keys:
                print(table[j], file=tb)
        print("---HERE END OUTPUT")
        f1.close()
        view.close()
        db.close()
        tb.close()
        next_page = response.css('.table-recently-updated+div a::attr("href")').extract()
        if len(next_page) > 1:
            next_page = next_page[1]
        else:
            next_page = next_page[0]

        # print("~~next page: " + next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
