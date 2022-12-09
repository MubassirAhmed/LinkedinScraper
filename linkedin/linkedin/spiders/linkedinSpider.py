import scrapy
from scrapy.http import TextResponse
import requests

class linkedinSpider(scrapy.Spider):
    name = "linkedin"

    def start_requests(self):
        #url = "https://www.linkedin.com/jobs/search/?currentJobId=3335051477&geoId=105149290&location=Ontario%2C%20Canada&start={}"
        
        #? Real Jobs
        _SQL_Entry_RemoteCanada_24hrs ='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=SQL&location=Canada&locationId=&geoId=101174742&f_TPR=r86400&f_WT=2&position=1&pageNum=0&start={}'
        SQL_Any_RemoteCanada_24hrs ='x'
        
        _SQL_Entry_AnyToronto_24hrs = 'x'
        SQL_Any_AnyToronto_24hrs = 'x'
        
        #? Any Jobs
        _Any_Entry_RemoteCanada_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=&location=Canada&locationId=&geoId=101174742&f_TPR=r86400&f_E=2&f_WT=2&position=1&pageNum=0'
        Any_Any_RemoteCanada_24hrs = 'https://ca.linkedin.com/jobs/search?keywords=&location=Canada&locationId=&geoId=101174742&f_TPR=r86400&f_WT=2&position=1&pageNum=0'
        
        _Any_Entry_AnyToronto_24hrs = 'x'
        Any_Any_AnyToronto_24hrs = 'x'

        feederURL = Any_Any_RemoteCanada_24hrs
        
        #? Do entry roles for trial runs, but in actual runs, scan everything
        
        #TODO Today: 
        #? Scraper Stuff:
        #? Figure out how to scrape number of jobs from initial link and feed it in to the scraper
        #? Figure out trial runs
        #? Figure out final runs
        
        #? Figure out how to analyse this in jupyter notebooks
        #! obv filter for no to 0 experience - figure this out in kijiji analysis book
        #? apps/hour calc.
        #? common key-words

        
        #? filter by less apps to more apps
        
        
        #total_jobs = requests.get(
       #     'https://www.linkedin.com/jobs/search?keywords=SQL&location=Canada&locationId=&geoId=101174742&f_TPR=r86400&f_WT=2&position=1&pageNum=0')
        #total_jobs_r1 = TextResponse(body=total_jobs.content, url=url)
        #total_jobs_resp = total_jobs_r1.css('span.results-context-header__job-count::text').extract()
        #clean_total_jobs = int(" ".join(total_jobs_resp).strip().replace("+", "").replace(",", ""))
        totalJobs = int(TextResponse(body=requests.get(feederURL).content, url=feederURL).css('span.results-context-header__new-jobs::text').get().strip().replace("\xa0new",'').replace("(","").replace(',','').replace(')',''))

        #? if there are 402 jobs, the page will load if you pass '400' as the parameter, but not '425'. However, it loads if you put '402', so this way you can get the last few jobs. You can put a second for loop just for those last few, but you may need another parse func for that.
        for i in range(0, totalJobs, 25):
            yield scrapy.Request(url=feederURL.replace("/jobs/", "/jobs-guest/jobs/api/seeMoreJobPostings/") + "&start={}".format(i),  # meta = {
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
        #job_desc = response.css('div.show-more-less-html__markup ::text').extract()
        clean_desc = " ".join(response.css('div.show-more-less-html__markup ::text').extract()).strip().lower()
        
        #criterion = response.css('span.description__job-criteria-text::text').get().strip().lower()
        clean_criterion = response.css('span.description__job-criteria-text::text').get().strip().lower()
        
        postedTimeAgo =  response.css('span.posted-time-ago__text::text').get().strip().lower()
        
        if any(word in postedTimeAgo for word in ['hour','hours']):
            postedTimeAgo = int(postedTimeAgo.replace("hours ago",'').replace("hour ago",'').strip())
        else:
        
            if any(word in postedTimeAgo for word in ['minutes','minute']):
                postedTimeAgo = int(postedTimeAgo.replace("minute ago",'').replace("minutes ago",'').strip())/60
            else: 
                if any(word in postedTimeAgo for word in ['day','days']):
                    postedTimeAgo = int(postedTimeAgo.replace("day ago",'').replace("days ago",'').strip())*24
    
            
        
        noApplicants = response.css('.num-applicants__caption::text').get().strip().lower()
        if 'among' in noApplicants:
            noApplicants = 0
        else:
            noApplicants = int(noApplicants.replace("applicants",'').replace("over",''))
            
        appsPerHr = noApplicants/postedTimeAgo
        #job_title = response.css('h1.topcard__title::text').get()
        clean_title = response.css('h1.topcard__title::text').get().strip().lower()
         
        #company = response.css('a.topcard__org-name-link::text').get()
        clean_company = response.css('a.topcard__org-name-link::text').get().strip().lower()
        
        #type_of_job = response.css('span.description__job-criteria-text::text').get()
        clean_type_of_job = response.css('span.description__job-criteria-text::text').get().strip().lower()
        
        #location = response.css('span.topcard__flavor::text').get()
        #clean_loc = "".join(response.css('span.topcard__flavor::text').getall()).strip().replace(",", "|")
                

        #dates_list = response.meta.get('dates_list')
        
        #industry = response.css('span.description__job-criteria-text::text').get()
        clean_industry = response.css('span.description__job-criteria-text::text').get().strip().lower()

        # try:
        #   date_posted = dates_list[0]
        #  dates_list.pop(0)
        # except:
        #   pass

        yield {'title': clean_title, 'appsPerHour': appsPerHr, 'typeOfJob': clean_type_of_job, 'job_link': response.request.url,
                'company': clean_company, 'industry': clean_industry, 'description': clean_desc,
                'criterion': clean_criterion} #, 'location': clean_loc, 'time_posted': clean_time}  # ,
        # 'datePosted':date_posted}

        #yield all_items

