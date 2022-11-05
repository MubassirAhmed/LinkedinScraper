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
        total_jobs = requests.get('https://www.linkedin.com/jobs/search/?currentJobId=3335051477&geoId=105149290&location=Ontario%2C%20Canada&start=0')
        total_jobs_r1 = TextResponse(body=total_jobs.content, url=url)
        total_jobs_resp =total_jobs_r1.css('span.results-context-header__job-count::text').extract()
        clean_total_jobs = int(" ".join(total_jobs_resp).strip().replace("+","").replace(",",""))

        for i in range(0, clean_total_jobs, 25):
            yield scrapy.Request(url=url.format(i),meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [302]
              }, callback=self.after_fetch)
            

    def after_fetch(self, response):
        dates_list = response.xpath('//time[@class="job-search-card__listdate"]/@datetime').getall()
        job_link = response.css('a.base-card__full-link::attr(href)').extract()

        for link in job_link:
            yield response.follow(url=link,
                                  callback=self.parse,
                                  meta={'dates_list':dates_list})

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
        clean_criterion = " ".join(crit.strip() for crit in criterion).strip().lower()        #                                              clean_title = " ".join(job_title).strip().lower()
        clean_desc = " ".join(job_desc).strip().lower()
        clean_company = " ".join(company).strip().lower()
        clean_loc = " ".join(loc).strip().replace(",", "|")
        clean_time = " ".join(time).strip()
        try:
            date_posted = dates_list[0]
            dates_list.pop(0)
        except:
            pass

        all_items = {'title': clean_title, 'typeOfJob':clean_type_of_job, 'job_link':response.request.url,
                     'company': clean_company, 'industry':clean_industry, 'description': clean_desc,
                     'criterion': clean_criterion, 'location': clean_loc, 'time_posted': clean_time,
                     'datePosted':date_posted}

        yield all_items