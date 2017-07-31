from __future__ import print_function

import scrapy
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class QuotesSpider1(scrapy.Spider):
    handle_httpstatus_list = [404]
    # name of spider
    name = "quotes1"
    animeCount = 34815
    # initial url
    start_urls = [
        'https://myanimelist.net/anime/1',
    ]

    # function is automatically called
    def parse(self, response):
        # data is stored in this file
        tb = open('./tb', 'a+')
        # list of members page links
        mem = open('./members', 'a+')
        # unvisited/error pages
        unv = open('./unvisited', 'a+')
        # missing attributes
        missing = "?"

        # In case page gives 404
        if response.status == 404:
            next_page = self.giveurl(response.url)
            # print("~~next page: " + next_page)
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page,
                                     callback=self.parse,
                                     errback=self.errback_httpbin)
            return
        # member page link
        stat = response.css('#horiznav_nav ul li:nth-child(6) a::attr(href)')
        print(stat.extract()[0].encode('utf-8'), file=mem)
        resp = response.css('div.js-scrollfix-bottom')

        # get side table
        div = resp.css('div')[0]
        # print(str(div), file=db)
        if len(div.css('.dark_text')) > 0:
            keys = ["English:", "Rating:", "Members:", "Ranked:", "Producers:", "Premiered:", "Studios:",
                   "Favorites:", "Aired:","Japanese:",
                   "Licensors:", "Status:", "Genres:", "Popularity:", "Duration:", "Type:", "Source:",
                   "Synonyms:", "Broadcast:", "Episodes:", "Score:"]
            # before score is count of users who scored
            # Get Key-Value pairs
            rawer_list = div.css(':not(h2):not(small):not(script)::text').extract()

            # create new list
            raw_list = list()

            for j in rawer_list:
                s = str(j.encode('utf-8')).strip()
                if len(s) > 0:
                    raw_list.append(s)
            # print(keys, file=db)
            # print(raw_list, file=view)
            # empty dictionary
            table = dict()

            # Puts values in dictionary with corresponding keys
            for j in range(0, len(raw_list)):
                s = raw_list[j]

                if len(s) > 0:
                    # print("kv: " + str(j.encode('utf-8')))
                    # print(s, file=f2)
                    if s in keys:
                        v = ""
                        j += 1

                        # print(s + " is in keys", file=db)

                        # get value, -1 means start from beginning
                        while raw_list[j][-1] != ':':
                            v += (raw_list[j] + " ")
                            j += 1
                            if j == len(raw_list):
                                break
                        j -= 1
                        # print(s+":"+v, file=db)
                        # remove single and double quotes
                        table[s] = re.sub('[\'\"]', '', v.strip())
                else:
                    print(response.url, file=unv)

            # remove last element in keys
            keys = keys[:len(keys) - 1]
            # Print to file
            # put the anime number(the nmber at end of url) in file
            print(response.url[(response.url.rfind("/") + 1):], end='|', file=tb)
            # output to file
            for j in keys:
                if j in table:
                    if j == "Ranked:":
                        table[j] = table[j][1:table[j].find(" ")]
                    print(table[j], end='|', file=tb)
                else:
                    print(missing, end='|', file=tb)
            if "Score:" in table:
                j = "Score:"
                print(table[j][table[j].find("scored by ")+10:table[j].find(" users")], end='|', file=tb)
                table[j] = table[j][0:table[j].find(" ")]
                print(table[j], file=tb)
            else:
                print(missing, file=tb)
        else:
            print(response.url, file=unv)

        tb.close()
        mem.close()
        unv.close()
        next_page = self.giveurl(response.url)
        # print("~~next page: " + next_page)
        # next page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,
                                 callback=self.parse,
                                 errback=self.errback_httpbin)
    # next url
    def giveurl(self, url):
        next_page = url
        i = next_page.rfind("/") + 1
        return next_page[:i] + str((int(next_page[i:]) + 1))

    # error handling functions
    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('lalalHttpError on %s', response.url)
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