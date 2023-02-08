import scrapy
from scrapy.http import TextResponse
import requests
import re
#from fake_useragent import UserAgent
#from selenium import webdriver
#import time 

class linkedinSpider(scrapy.Spider):
    
    name = "linkedin"
    
    # custom_settings = {
    #     'FEEDS': { "s3://linkedin-scraper-1/%(name)s/%(name)s_%(time)s.csv" : {"format": "csv"} }
    # }

    
    def start_requests(self):              
        feederURL = 'https://www.linkedin.com/jobs/search/?currentJobId=3461656172&f_TPR=r86400&geoId=101174742&keywords=%22analyst%22%20AND%20(%22python%22%20OR%20%22sql%22)&location=Canada&refresh=true'   
        for i in range(0, 25, 25):
            yield scrapy.Request(url=feederURL.replace("/jobs/",
                                    "/jobs-guest/jobs/api/seeMoreJobPostings/") 
                                    + "&start={}".format(i),
                                callback=self.after_fetch)
        

    def after_fetch(self, response):
        job_link = response.css('a.base-card__full-link::attr(href)').extract()

        for link in job_link:
            yield response.follow(url=link,
                                  callback=self.parse) 

    def parse(self, response, **kwargs):
        postedTimeAgo =  response.css('span.posted-time-ago__text::text').get().strip().lower()
        if any(word in postedTimeAgo for word in ['hour','hours']):
            postedTimeAgo = int(postedTimeAgo.replace("hours ago",'').replace("hour ago",'').strip())
        else:
            if any(word in postedTimeAgo for word in ['minutes','minute']):
                postedTimeAgo = int(int(postedTimeAgo.replace("minute ago",'').replace("minutes ago",'').strip())/60)
            else: 
                if any(word in postedTimeAgo for word in ['day','days']):
                    postedTimeAgo = int(postedTimeAgo.replace("day ago",'').replace("days ago",'').strip())*24
                    
        noApplicants = response.css('.num-applicants__caption::text').get().strip().lower()
        if 'among' in noApplicants:
            noApplicants = 0
        else:
            noApplicants = int(noApplicants.replace("applicants",'').replace("over",''))   
            
        # appsPerHr = noApplicants/postedTimeAgo
        clean_title = response.css('h1.topcard__title::text').get().strip().lower()
        clean_company = response.css('a.topcard__org-name-link::text').get().strip().lower()
    
        jobMetaData = len(response.css('span.description__job-criteria-text::text').getall())
        if jobMetaData >= 1:
            clean_seniority_level = response.css('span.description__job-criteria-text::text').getall()[0].strip().lower()
        else:
            clean_seniority_level = 'n/a'
        if jobMetaData >= 2:
            clean_employment_type = response.css('span.description__job-criteria-text::text').getall()[1].strip().lower()
        else:
            clean_employment_type = 'n/a'

        if jobMetaData >= 3:
            clean_job_function = response.css('span.description__job-criteria-text::text').getall()[2].strip().lower()
        else:
            clean_job_function = 'n/a'

        if jobMetaData >= 4:
            clean_industry = response.css('span.description__job-criteria-text::text').getall()[3].strip().lower()
        else:
            clean_industry = 'n/a'

        job_link = response.request.url
        clean_desc = " ".join(response.css('div.show-more-less-html__markup ::text').extract()).strip().lower()  
        job_id = int(re.findall("\d{10}",job_link)[0])
        

        company_link = response.css('a.topcard__org-name-link::attr(href)').get().replace('?trk=public_jobs_topcard-org-name','/?originalSubdomain=ca')
        
#   #     yield response.follow(url=company_link,
    #                           headers = {
    #                               "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #                               "accept-encoding" : "gzip, deflate, sdch, br",
    #                               "accept-language" : "en-US,en;q=0.8,ms;q=0.6",
    #                               "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    #                            },
    #                          callback=self.parse_company)
    #    #ua = UserAgent(verify_ssl=False)
        #user_agent = ua.random
        #chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("user-agent=" + user_agent)
        #driver = webdriver.Chrome(chrome_options=chrome_options)
        #driver.get(company_link)
        #time.sleep(1)


        yield {'title': clean_title, 
               #'appsPerHour': appsPerHr,
               'noApplicants': noApplicants,
               'postedTimeAgo':postedTimeAgo,
               'company': clean_company,
               'job_link': job_link,
               'description': clean_desc,
               'seniorityLevel':clean_seniority_level,
               'employmentType':clean_employment_type,
               'jobFunction':clean_job_function,
               'industry':clean_industry,
               'job_id': job_id
                }

    def parse_company(self,response):
        yield{'company_industry': response.css('h2.top-card-layout__headline::text').get().strip().lower()}
            

