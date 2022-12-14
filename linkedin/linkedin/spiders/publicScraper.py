#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 19:11:09 2022

@author: mvbasxhr
"""


import scrapy
from scrapy.http import TextResponse
import requests

class PublicSpider(scrapy.Spider):
    name = "PublicSpider"




    def start_requests(self):
        url = "https://www.linkedin.com/jobs/search/?currentJobId=3335051477&geoId=105149290&location=Ontario%2C%20Canada&start={}"
        total_jobs = requests.get(
            'https://www.linkedin.com/jobs/search/?currentJobId=3335051477&geoId=105149290&location=Ontario%2C%20Canada&start=0')
        total_jobs_r1 = TextResponse(body=total_jobs.content, url=url)
        total_jobs_resp = total_jobs_r1.css('span.results-context-header__job-count::text').extract()
        clean_total_jobs = int(" ".join(total_jobs_resp).strip().replace("+", "").replace(",", ""))

        for i in range(0, clean_total_jobs, 25):
            yield scrapy.Request(url=url.format(i),  # meta = {
                                 #   'dont_redirect': True,
                                 #   'handle_httpstatus_list': [303]},
                                 callback=self.after_fetch)

    def after_fetch(self, response):
        # dates_list = response.xpath('//time[@class="job-search-card__listdate"]/@datetime').getall()
        job_link = response.css('a.base-card__full-link::attr(href)').extract()

        for link in job_link:
            yield response.follow(url=link,
                                  callback=self.parse)  # ,
            # meta={'dates_list':dates_list})

    def parse(self, response, **kwargs):
        job_desc = response.css('div.show-more-less-html__markup ::text').extract()
        criterion = response.css('span.description__job-criteria-text::text').extract()
        job_title = response.css('h1.topcard__title::text').extract()
        company = response.css('a.topcard__org-name-link::text').extract()
        loc = response.css('span.topcard__flavor::text').extract()
        time = response.css('span.posted-time-ago__text::text').extract()
        dates_list = response.meta.get('dates_list')
        industry = response.css('span.description__job-criteria-text::text').getall()[2]
        type_of_job = response.css('span.description__job-criteria-text::text').getall()[3]

        clean_type_of_job = type_of_job.strip().lower()
        clean_industry = industry.strip().lower()
        clean_title = " ".join(job_title).strip().lower()
        clean_criterion = " ".join(
            crit.strip() for crit in criterion).strip().lower()  # clean_title = " ".join(job_title).strip().lower()
        clean_desc = " ".join(job_desc).strip().lower()
        clean_company = " ".join(company).strip().lower()
        clean_loc = " ".join(loc).strip().replace(",", "|")
        clean_time = " ".join(time).strip()
        # try:
        #   date_posted = dates_list[0]
        #  dates_list.pop(0)
        # except:
        #   pass

        all_items = {'title': clean_title, 'typeOfJob': clean_type_of_job, 'job_link': response.request.url,
                     'company': clean_company, 'industry': clean_industry, 'description': clean_desc,
                     'criterion': clean_criterion, 'location': clean_loc, 'time_posted': clean_time}  # ,
        # 'datePosted':date_posted}

        yield all_items



class KijijiSpider(scrapy.Spider):
    name = "kijiji"
   # HEADERS = {
    #    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
     #   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      #  "Accept-Language": "en-US,en;q=0.5",
#        "Accept-Encoding": "gzip, deflate",
 #       "Connection": "keep-alive",
  #      "Upgrade-Insecure-Requests": "1",
   #     "Sec-Fetch-Dest": "document",
    #    "Sec-Fetch-Mode": "navigate",
     #   "Sec-Fetch-Site": "none",
      #  "Sec-Fetch-User": "?1",
#        "Cache-Control": "max-age=0",
 #   }

    def start_requests(self):
        url = 'https://www.kijiji.ca/b-room-rental-roommate/city-of-toronto/page-{}/c36l1700273?radius=25.0&ad=offering&price=__700&address=East+York%2C+Toronto%2C+ON&ll=43.691201,-79.341664'
        for i in range(1, 2):
            yield scrapy.Request(url=url.format(i), callback=self.after_fetch)  #, headers = HEADERS)

    def after_fetch(self, response):
        posting_links = response.css('a.title::attr(href)').extract()

        for link in posting_links:
            yield response.follow(url=link,
                                  callback=self.parse) #, headers = HEADERS)  # ,

#testing css selectors
#scrapy shell 'url'
#>>>response.css('a.span::text').get()
#[0] 'good'

    def parse(self, response):
#        desc = response.css('p ::text').extract()
#        title = " ".join(response.css('h1 ::text').extract()).strip().lower()
         #crit.strip() for crit in criterion).strip().lower()  # clean_title = " ".join(job_title).strip().lower()
#        clean_desc = " ".join(response.css('p ::text').extract()).strip().lower().replace('\n',' ')
#        all_items = {'title':title, 'url': response.request.url, 'description': clean_desc}

#        yield all_items
        yield {'title': response.css('h1 ::text').get().strip().lower(),
               'price': response.css('[class^="priceContainer"]').css('span::text').get(),
               'url': response.request.url,
               'description': " ".join(response.css('p ::text').getall()).strip().lower().replace('\n',' '),           
        }
        
#def parse(self, response):
#    for wines in response.css('div.txt-wrap'):
#        yield {'name': wines.css('a::text').get(),
#               'price': wines.css('strong.price::text').get().replace('$ ',''),
#               'link': wines.css('a').attrib['href'],
#               }

class cSpider(scrapy.Spider):
    name = "c"

    def start_requests(self):
        url='https://www.c.com/search.php?st=0&sk=t&sd=d&sr=topics&keywords={keyword}ight&sf=titleonly&start={pageNumber}'
        keyword =''
        url=url.format(keyword)
        for pageNumber in range(0, 2325, 75):
        #for i in range(0, 5250, 75):
            yield scrapy.Request(url=url.format(pageNumber))


    def parse(self, response):
        topic_links = response.css('a.topictitle::attr(href)').extract()
        topic_views = response.css('dd.views::text').extract()
        topic_views.pop(0)
        
        for i in range(0,75):
            print(topic_views[i] + " " + "https://www.c.com"+ topic_links[i][1:])
            yield { 'url': "https://www.c.com/"+topic_links[i][1:],
                    'views': int(topic_views[i])
            }

