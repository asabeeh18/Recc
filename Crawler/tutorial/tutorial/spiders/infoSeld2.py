from __future__ import print_function

import scrapy
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class QuotesSpider1(scrapy.Spider):
    name = "quotes1"
    animeCount = 34815
    start_urls = [
        'https://myanimelist.net/anime/1',
    ]
    def parse(self, response):
        tb = open('./tb', 'a+')
        mem = open('./members', 'a+')
        unv = open('./unvisited', 'a+')
        missing = "?"
        stat = response.css('#horiznav_nav ul li:nth-child(6) a::attr(href)')

        print(stat.extract()[0].encode('utf-8'), file=mem)
        resp = response.css('div.js-scrollfix-bottom')

        div = resp.css('div')[0]
        # print(str(div), file=db)
        if len(div.css('.dark_text')) > 0:
            keys = ["English:", "Rating:", "Members:", "Ranked:", "Producers:", "Premiered:", "Studios:",
                   "Favorites:", "Aired:","Japanese:",
                   "Licensors:", "Status:", "Genres:", "Popularity:", "Duration:", "Type:", "Source:",
                   "Synonyms:", "Broadcast:", "Episodes:", "Score:"]
            # values
            rawer_list = div.css(':not(h2):not(small):not(script)::text').extract()
            # print(rawer_list,file=view)

            raw_list = list()

            for j in rawer_list:
                s = str(j.encode('utf-8')).strip()
                if len(s) > 0:
                    raw_list.append(s)
            # print(keys, file=db)
            # print(raw_list, file=view)
            table = dict()
            for j in range(0, len(raw_list)):
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
                        # print(s+":"+v, file=db)
                        table[s] = re.sub('[\'\"]', '', v.strip())
                else:
                    print(response.url, file=unv)

            keys = keys[:len(keys) - 1]
            # Print to file
            print(response.url[(response.url.rfind("/") + 1):], end='|', file=tb)
            for j in keys:
                if j in table:
                    print(table[j], end='|', file=tb)
                else:
                    print(missing, end='|', file=tb)
            if "Score:" in table:
                print(table["Score:"], file=tb)
            else:
                print(missing, file=tb)
        else:
            print(response.url, file=unv)

        tb.close()
        mem.close()
        unv.close()
        next_page = self.giveurl(response.url)
        # print("~~next page: " + next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,
                                 callback=self.parse,
                                 errback=self.errback_httpbin)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            next_page = self.giveurl(response.url)
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page,
                                     callback=self.parse,
                                     errback=self.errback_httpbin)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

        else:
            response = failure.value.response

    def giveurl(self, url):
        next_page = url
        i = next_page.rfind("/") + 1
        return next_page[:i] + str((int(next_page[i:]) + 1))
