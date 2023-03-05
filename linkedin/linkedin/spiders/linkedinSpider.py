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
        #past 24 hrs
        analyticsANDsql = 'https://www.linkedin.com/jobs/search/?currentJobId=3467060936&f_TPR=r86400&geoId=101174742&keywords=analytics%20and%20sql&location=Canada&refresh=true'

        analystAND_sqlORpython_ = 'https://www.linkedin.com/jobs/search?keywords=Analyst%20And%20%28sql%20Or%20Python%29&location=Canada&locationId=&geoId=101174742&sortBy=R&f_TPR=r86400&position=1&pageNum=0'

        #!Initial loading
        #past week

        #analystAND_sqlORpython
        canada_pastWeek = 'https://www.linkedin.com/jobs/search?keywords=Analyst%20And%20%28sql%20Or%20Python%29&location=Canada&locationId=&geoId=101174742&f_TPR=r604800&position=1&pageNum=0'
        
        #analytics_andSQL_notIntern 'analytics' returns wayy more results so I'm splitting it into provinces

        novaScotia_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql&location=nova%20scotia&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        ontario_pastWeek = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=Ontario%2C%20Canada&locationId=&geoId=105149290&sortBy=R&f_TPR=r604800&position=1&pageNum=0'

        alberta_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=Alberta&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        manitoba_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=Manitoba&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        saskatchewan_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=Saskatchewan&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        BC_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20Sql%20NOT%20Intern&location=British%20Columbia&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        Quebec_anyTime = 'https://www.linkedin.com/jobs/search?keywords=Analytics%20AND%20python%20NOT%20Intern&location=Quebec&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

        AD_HOC = 'https://www.linkedin.com/jobs/search/?currentJobId=3482844494&f_TPR=r604800&geoId=101174742&keywords=%22sql%22%20or%20%22python%22&location=Canada&refresh=true&sortBy=R'

        economics ='https://www.linkedin.com/jobs/search?keywords=%22analyst%22%2Band%2B%22economics%22&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=3313052700&position=1&pageNum=0'

        analyst_or_sql_past_week = 'https://www.linkedin.com/jobs/search?keywords=%22analyst%22%2BAnd%2B%22sql%22&location=Canada&geoId=101174742&f_TPR=r604800&currentJobId=3493934649&position=2&pageNum=0'
        new ='https://www.linkedin.com/jobs/search?keywords=Underwriting&location=Canada&geoId=101174742&f_TPR=r604800&currentJobId=3494387464&position=13&pageNum=0'

        #################################################################
        ########################Weekly#########################################


        keywords = ["excel"]
        provinces = ['Nova Scotia', 'Manitoba','Saskatchewan', 'New Brunswick', 'Prince Edward Island', 'Newfoundland and Labrador', 'Ontario', 'Quebec', 'Alberta', 'British Columbia']
        #provinces = ['Prince%20Edward%20Island','Newfoundland%20and%20Labrador','New%20Brunswick','Saskatchewan']
        
        time = {'week' : 'r604800', 'month' : 'r2592000' }

        geoIds = ['104823201', '104423466', '104002611', '103790618',
                  '104663945', '106199678','105149290', '102237789', '103564821','102044150']

        for keyword in keywords:
            for index, province in enumerate(provinces):
                feederURL = 'https://www.linkedin.com/jobs/search?keywords={}&location={}%2C%20Canada&geoId={}&f_TPR={}&position=1&pageNum=0'.format(keyword.replace(" ","%20").replace("\"","%22"), province, geoIds[index], time["month"])
                
                totalJobs = int(TextResponse(body=requests.get(feederURL).content, url=feederURL).css('span.results-context-header__job-count::text').get().replace('+','').replace(',',''))

                #totalJobs = 25
                for i in range(0, totalJobs, 25):
                    yield scrapy.Request(url=feederURL.replace("/jobs/",
                                            "/jobs-guest/jobs/api/seeMoreJobPostings/") 
                                            + "&start={}".format(i),
                                        callback=self.after_fetch,
                                        meta={'province': province.replace("%20"," ")})
                # remove to loop over feederURLs
                #break


        # feederURL = 'https://www.linkedin.com/jobs/search?keywords=Excel%20Or%20Degree&location=Toronto%2C%20Ontario%2C%20Canada&locationId=&geoId=100761630&f_TPR=r604800&distance=10&position=1&pageNum=0'
                
        # totalJobs = int(TextResponse(body=requests.get(feederURL).content, url=feederURL).css('span.results-context-header__job-count::text').get().replace('+','').replace(',',''))

        # #totalJobs = 25
        # for i in range(0, totalJobs, 25):
        #     yield scrapy.Request(url=feederURL.replace("/jobs/",
        #                             "/jobs-guest/jobs/api/seeMoreJobPostings/") 
        #                             + "&start={}".format(i),
        #                         callback=self.after_fetch,)
                                #meta={'province': province.replace("%20"," ")})
        # remove to loop over feederURLs
        #break

    def after_fetch(self, response):
        job_link = response.css('a.base-card__full-link::attr(href)').extract()

        for link in job_link:
            yield response.follow(url=link,
                                  meta={'province' : response.meta['province']},
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

        clean_city =  response.css('span.topcard__flavor.topcard__flavor--bullet::text').get().strip().lower().replace(',',"").split()[0]

        job_link = response.request.url
        clean_desc = " ".join(response.css('div.show-more-less-html__markup ::text').extract()).strip().lower()  
        job_id = clean_title + clean_company + clean_industry + clean_job_function
        

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
               'job_id': job_id,
               'city': clean_city,
               'province': response.meta['province'],
                }

    def parse_company(self,response):
        yield{'company_industry': response.css('h2.top-card-layout__headline::text').get().strip().lower()}
            

