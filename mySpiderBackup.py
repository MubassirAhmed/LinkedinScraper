#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 22:27:51 2022

@author: mvbasxhr
"""

import scrapy


class PublicSpider(scrapy.Spider):
    name = "generalBackupSpider"

    def start_requests(self):
        
        url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?currentJobId=3335051477&geoId=105149290&location=Ontario%2C%20Canada&start={}"

        for i in range(0,25,25):
            yield scrapy.Request(url=url.format(i), callback=self.after_fetch)


    def after_fetch(self, response):
        dates_list = response.xpath('//time[@class="job-search-card__listdate"]/@datetime').getall()
        job_link = response.css('a.base-card__full-link::attr(href)').extract()
        print(dates_list)
        dates_list = 'fk'
        print(dates_list)
        print('lolwatthefuckSSs')
        yield response.follow(
            url=link,
            callback=self.parse),
          #  meta={'dates_list': dates_list})
#in after_fetch method:
#    dates_list = response.xpath('//time[@class="job-search-card__listdate"]/@datetime').getall()
#    yield response.follow(url=link, callback=self.parse, meta={
#        'date_list': dates_list})
#----------
#in parse method:
    #

    def parse(self, response, **kwargs):
        
         criterion = response.css('span.description__job-criteria-text::text').extract().lower()
         job_desc = response.css('div.show-more-less-html__markup ::text').extract().lower()
         title = response.css('h1.topcard__title::text').extract().lower()
         company = response.css('a.topcard__org-name-link::text').extract()
         loc = response.css('span.topcard__flavor::text').extract()
         time = response.css('span.posted-time-ago__text::text').extract()
         dates_list = response.meta.get('dates_list')

         date_posted = dates_list(0)
         dates_list.pop(0)
#         date = response.xpath('//time[@class="main-job-card__listdate"]/@datetime').extract_first()
  

                     
         clean_desc = " ".join(job_desc).strip().replace(",", "|")
         clean_criterion = " ".join(crit.strip() for crit in criterion).strip().replace(",", "|")
         clean_title = " ".join(title).strip()
         clean_company = " ".join(company).strip()
         clean_loc = " ".join(loc).strip().replace(",", "|")
         clean_time = " ".join(time).strip()
         
         
         all_items = {'title': clean_title, 'job_link':response.request.url, 
                      'company': clean_company,'description':clean_desc,
                      'criterion': clean_criterion, 'location': clean_loc, 
                      'time_posted': clean_time, 'date_posted':date_posted}         
         yield all_items


        
# =============================================================================
#         import json
# 
#         def read_json_file(file):
#             with open(file, "r") as r:
#                 response = r.read()
#                 response = response.replace('\n', '')
#                 response = response.replace('][', ',')
#                 response = "[" + response[1:-1] + "]"
#                 return json.loads(response)
#             
# 
#         read_json_file('/Users/mvbasxhr/Cool Stuff/LinkedInScraper/linkedin/linkedin/spiders/master_jobs_list.json')
# =============================================================================
# =============================================================================
# from scrapy import Selector
# from scrapy.shell import inspect_response
# #from selenium import webdriver
# #from selenium.webdriver.common.keys import Keys
# 
# import datetime 
# 
# 
# # Creating a spider class 
# 
# class MySpider(scrapy.Spider): 
#     name = 'myspider' 
# 
#     allowed_domains = ['linkedin.com'] 
#     
# #TODO
# #allow to pass in keywords & job location rather than hardcoding it    
#     start_urls=['https://www.linkedin.com/jobs/search/?currentJobId=3335051477&geoId=105149290&location=Ontario%2C%20Canada&refresh=true']
# 
# 
# 'https://www.linkedin.com/jobs/search/?currentJobId=3335051477&geoId=105149290&location=Ontario%2C%20Canada&refresh=true&trk=public_jobs_jobs-search-bar_search-submit&start={}'
# 
# 'https://www.linkedin.com/jobs/search/?currentJobId=3335051477&geoId=105149290&location=Ontario%2C%20Canada&start={}'
# 
# # this function will request the websites and feed it to parse method 
# 
# def start_requests(self):
#     for url in self.start_urls:
#         yield scrapy.Request(url, self.parse, 
#                              meta={'splash': {
#                                      'endpoint': 'render.html',
#                                      'args': {'wait': 0.5} 
#                                      }})
#  
# 
# # We can write our code logic inside parse method 
# 
# def parse(self, response):
#     inspect_response(response, self)
#     
#     #driver = webdriver.Chrome()
# # Use headless option to not open a new browser window
# # =============================================================================
# #     options = webdriver.ChromeOptions()
# #     options.add_argument("headless")
# #     desired_capabilities = options.to_capabilities()
# #     driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
# #     
# #     driver.get()
# # 
# #  # creating an empty list, in which we will save data later 
# # =============================================================================
#     
# this contains the link & name of the job
# <a data-control-id="8ObYQPiPSaL2EN1bhhMCsQ==" tabindex="0" href="/jobs/view/3322693679/?eBP=JOB_SEARCH_ORGANIC&amp;recommendedFlavor=SCHOOL_RECRUIT&amp;refId=hUm%2F9ZwnAUId6gwPgvr4qQ%3D%3D&amp;trackingId=8ObYQPiPSaL2EN1bhhMCsQ%3D%3D&amp;trk=flagship3_search_srp_jobs" id="ember192" class="disabled ember-view job-card-container__link job-card-list__title">
#               Application Support Engineer
#             </a>
#             
#             
#             
#             this contains name of company
#             <a href="/company/19082327/" id="ember194" class="job-card-container__link job-card-container__company-name ember-view">
#               Pivotree
#             </a>
#             
#             
#             
# Location +  remote/onsite/hybrid : this needs chaining
# 
# <div id="ember195" class="artdeco-entity-lockup__caption ember-view">
#             <ul class="job-card-container__metadata-wrapper">
#                 <li class="job-card-container__metadata-item">Ontario, Canada</li>
#                 <li class="job-card-container__metadata-item job-card-container__metadata-item--workplace-type">
#                   On-site
#                 </li>
#             </ul>
#       </div>
# 
# 
# 
# 
# no.of alumni (not always available)
# 
# 
# <div class="job-flavors__flavor job-flavors__flavor--school-recruit">
#     <a href="/search/results/people/?currentCompany=19082327&amp;origin=JOB_PAGE_CANNED_SEARCH&amp;schoolFilter=10875" id="ember197" class="search-s-shared-connections__link job-flavors__link link-without-visited-state ember-view">
#       <div class="job-flavors__logo-container">
#           <img title="University of Waterloo" src="https://media-exp1.licdn.com/dms/image/C560BAQFI41Ly6leq7Q/company-logo_100_100/0/1519896484763?e=1675296000&amp;v=beta&amp;t=DoHMQ7VQwLjzW7X_RAI60LXrYhas3M10hzPH0wqKEWM" loading="lazy" alt="University of Waterloo" id="ember198" class="job-flavors__logo-image lazy-image ember-view">
#       </div>
# 
#       <div class="job-flavors__label t-12 t-black--light t-normal">
#         6 alumni work here
#       </div>
#     </a>
# </div>
# 
# 
# 
# day of posting
# =============================================================================
# ("//time[@class='main-job-card__listdate']").get_attribute("datetime")
# response.xpath('//time[@class="main-job-card__listdate"]/@datetime').extract_first()
# .time ::attr
# # 
# =============================================================================
# <ul class="job-card-list__footer-wrapper job-card-container__footer-wrapper flex-shrink-zero display-flex t-sans t-12 t-black--light t-normal t-roman">
#             <li class="job-card-container__listed-time job-card-container__footer-item
#                 ">
#               <time datetime="2022-10-16">
#                 1 week ago
# 
# <!---->              </time>
#             </li>
#           
#             <li class="job-card-container__applicant-count job-card-container__footer-item job-card-container__footer-item--highlighted t-bold inline-flex align-items-center">
#               0 applicants
#             </li>
# 
# <!---->    </ul>
# 
# 
# 
# After following link
# 
# this has entry level / mid senior etc & full-time/part time/contract & industry
# 
# <div class="mt5 mb2">
#           <ul>
#                 <li class="jobs-unified-top-card__job-insight">
#                   <div class="flex-shrink-zero mr2 t-black--light">
#                     <div class="ivm-image-view-model   ">
#     <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
#     
#     ">
#     <li-icon aria-hidden="true" type="job" size="large"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" data-supported-dps="24x24" fill="currentColor" class="mercado-match" width="24" height="24" focusable="false">
#   <path d="M17 6V5a3 3 0 00-3-3h-4a3 3 0 00-3 3v1H2v4a3 3 0 003 3h14a3 3 0 003-3V6zM9 5a1 1 0 011-1h4a1 1 0 011 1v1H9zm10 9a4 4 0 003-1.38V17a3 3 0 01-3 3H5a3 3 0 01-3-3v-4.38A4 4 0 005 14z"></path>
# </svg></li-icon>
# </div>
#   </div>
#                   </div>
#                   <span>
#                     <!---->Full-time · Entry level<!---->
#                   </span>
#                 </li>
#                 <li class="jobs-unified-top-card__job-insight">
#                   <div class="flex-shrink-zero mr2 t-black--light">
#                     <div class="ivm-image-view-model   ">
#     <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
#     
#     ">
#     <li-icon aria-hidden="true" type="company" size="large"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" data-supported-dps="24x24" fill="currentColor" class="mercado-match" width="24" height="24" focusable="false">
#   <path d="M4 2v20h16V2zm14 18h-4v-2h-4v2H6V4h12zm-7-8H8v-2h3zm0 4H8v-2h3zm5-4h-3v-2h3zm-5-4H8V6h3zm5 0h-3V6h3zm0 8h-3v-2h3z"></path>
# </svg></li-icon>
# </div>
#   </div>
#                   </div>
#                   <span>
#                     <!---->501-1,000 employees · IT Services and IT Consulting<!---->
#                   </span>
#                 </li>
#                 <li class="jobs-unified-top-card__job-insight">
#                   <div class="flex-shrink-zero mr2 t-black--light">
#                     <div class="ivm-image-view-model   ">
#     <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
#     
#     ">
#     <li-icon aria-hidden="true" type="people" size="large"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" data-supported-dps="24x24" fill="currentColor" class="mercado-match" width="24" height="24" focusable="false">
#   <path d="M12 16v6H3v-6a3 3 0 013-3h3a3 3 0 013 3zm5.5-3A3.5 3.5 0 1014 9.5a3.5 3.5 0 003.5 3.5zm1 2h-2a2.5 2.5 0 00-2.5 2.5V22h7v-4.5a2.5 2.5 0 00-2.5-2.5zM7.5 2A4.5 4.5 0 1012 6.5 4.49 4.49 0 007.5 2z"></path>
# </svg></li-icon>
# </div>
#   </div>
#                   </div>
#                   <span>
#                     <a class="app-aware-link " target="_self" href="https://www.linkedin.com/search/results/people/?origin=JOB_PAGE_CANNED_SEARCH&amp;currentCompany=%5B19082327%5D&amp;schoolFilter=%5B166688%5D" data-test-app-aware-link=""><!---->6 school alumni<!----></a>
#                   </span>
#                 </li>
# <!---->                <li class="jobs-unified-top-card__job-insight">
#                   <div class="flex-shrink-zero mr2 t-black--light">
#                     <div class="ivm-image-view-model   ">
#     <div class="ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex
#     
#     ">
#     <li-icon type="radar-screen" class="ivm-view-attr__icon--signal-positive " size="large" role="img" aria-label="Actively recruiting"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" data-supported-dps="24x24" fill="currentColor" class="mercado-match" width="24" height="24" focusable="false">
#   <path d="M12 20a8 8 0 010-16 7.91 7.91 0 014.9 1.69l-1.43 1.42a6 6 0 101.42 1.42l3.82-3.82a1 1 0 000-1.41A1 1 0 0020 3a1 1 0 00-.7.29l-1 1A10 10 0 1022 12h-2a8 8 0 01-8 8zm5-8a5 5 0 11-5-5 4.93 4.93 0 012.76.82l-2.24 2.24A2.24 2.24 0 0012 10a2 2 0 102 2 2.24 2.24 0 00-.07-.51l2.24-2.24A5 5 0 0117 12z"></path>
# </svg></li-icon>
# </div>
#   </div>
#                   </div>
#                   <span>
#                     <!---->Actively recruiting<!---->
#                   </span>
#                 </li>
#           </ul>
#               </div>
# 
# 
# 
# 
# Job description after following link
# 
# <div class="jobs-description__content jobs-description-content
#         jobs-description__content--condensed">
#       <div class="jobs-box__html-content jobs-description-content__text t-14 t-normal
#           jobs-description-content__text--stretch" id="job-details" tabindex="-1">
#           <h2 class="mt5 t-20 t-bold mb4">
#             About the job
#           </h2>
# 
# <!---->
# <!---->        <span>
#                 <strong><u>Introduction</u></strong><p><br>
# </p>Our goal at Pivotree is to help accelerate the future of frictionless commerce. We will help lead this change over the next decade because we believe a future where technology is embedded intimately into all aspects of our everyday lives can benefit everyone and will shape the interactions with the brands we love. We will help shape the future of frictionless commerce by working together with some of the best brands in the world and some of the best people in the industry to leverage converging technologies that will make it possible to accelerate frictionless commerce faster than ever.<p><br>
# </p>Pivotree provides services focused on the design, implementation, management, and maintenance of complex ecommerce solutions for large enterprises. We provide the technical skills necessary to enable the effective use of technologies combined with the business context to leverage a solution to solve our clients' business challenges. We strive to fill the gaps in available technology with our own IP to reduce the barriers to adoption.<p><br>
# </p>We enable inclusive, immersive and highly personalized experiences for our clients and their customers. We build our products with a view to productizing and scaling technology to lower the costs and reduce the risks of implementing and managing our integrated solutions. Each of our solutions starts with reliable and reputable e-commerce and MDM platforms, which run on enterprise grade infrastructure that are customized to meet a variety of client needs, situations, and budgets. Over the next 10 years we will add new categories and capabilities that will define frictionless commerce ecosystems.<p><br>
# </p>This is a journey of technology acceleration combined with consumer readiness and adoption. We are looking for people capable of adapting relentlessly to the rapidly evolving world around us.<p><br>
# </p><strong>Application Support Engineer</strong><p><br>
# </p><strong><u>Duties</u></strong><p><br>
# </p><ul><li>Perform software application engineering of eCommerce customer environments, providing environment build-out, troubleshooting and configuration Implementation and troubleshooting of middleware.</li><li>Migration and support of clients to cloud environments.</li><li>Work on both strategic short and long term issues and projects. Build strong relationships with clients at various levels and other Pivotree operations teams.</li><li>Interact with multiple departments on a regular basis, and the presentation of information to both technical and business stakeholders.</li><li>Tasked with providing engineering and hands on management with minimal oversight from the greater Pivotree organization.</li><li>Perform daily support tasks (support tickets, deployments, troubleshooting, etc…).</li><li>Work with end customers to improve and stabilize their applications.</li><li>Improve existing deployment and support processes.</li><li>Application improvements (deployment scripts, automation, application configuration etc.)</li><li>Participate in rotating on-call schedule.</li></ul><p><br>
# </p><strong><u>Requirements</u></strong><p><br>
# </p>Requires a Bachelor's degree in Computer Science, Computer Engineering, Mathematics, or a directly related field. Experienced linux operator, able perform required tasks efficiently within a linux environment. Ability to holistically review an application, identify and address issues real time. Previous experience with cloud projects/migrations (AWS, Azure). Proficient with ticking systems such as Atlassian service desk, jira. Candidates with Oracle Commerce (ATG) or other eCommerce application support is preferred but not required.<p><br>
# </p><strong> Application Environment Management </strong><p><br>
# </p><ul><li>Content Delivery Network (CDN) - akamai, cloudflare, others</li><li>Software/hardware load balancers</li><li>Certificate management - at CDN, webserver and application layers (keystores)</li><li>Ability to manage and troubleshoot traffic flow in/out of an environment</li><li>Support and analysis of environment performance/load tests</li></ul><p><br>
# </p><strong> Webserver experience: Apache or nginx </strong><p><br>
# </p><ul><li>Installation and configuration</li><li>Troubleshooting error codes</li><li>Rewrite / redirect rules</li></ul><p><br>
# </p><strong> Application server experience: Weblogic, jboss </strong><p><br>
# </p><ul><li>Installation and configuration</li><li>Troubleshooting application issues</li><li>Patching and updating</li></ul><p><br>
# </p><strong> Java application support </strong><p><br>
# </p><ul><li>Memory heap tuning, thread and heap dump analysis</li><li>Java application troubleshooting and support</li></ul><p><br>
# </p><strong><u>Relational Database Experience (MySQL, Oracle DB)</u></strong><p><br>
# </p><ul><li>Creating, reviewing, running sql</li><li>Exporting and importing of data</li><li>User creation and management</li></ul><p><br>
# </p>Pivotree is an equal opportunity employer. We celebrate diversity and are committed to creating an inclusive and accessible workplace.<p><br>
# </p>Apply Now
# <!---->        </span>
#       </div>
# <!---->      <div class="jobs-description__details">
# <!---->
#       </div>
#     </div>
# # =============================================================================
# #     for option in response.css("div.select-size select.sizeOptions option")[1:]:
# #         print(option.xpath("text()").extract())
# #         
# #     product_data = [] 
# # 
# #  # using css selector to select div 
# # 
# #     for card in response.css('.popular_regime-card'): 
# # 
# #  # don't forget to use exception handling 
# # 
# #         try: 
# # 
# #          product_name = card.css('.popular_prod-name::text').extract() 
# #         
# #          discounted = card.css('.popular_discount::text').extract() 
# #         
# #          mrp = card.css('.popular_mrp::text').extract() 
# #         
# #          price_details_dict = { 
# #         
# #          'discounted price': discounted, 
# #         
# #          'mrp': mrp 
# #                              } 
# # 
# #  
# #          product_dict = { 
# #         
# #          'product_name': product_name, 
# #         
# #          'price_details': price_details_dict 
# #         
# #          } 
# #          
# #              
# # 
# #         # saving all the data to earlier created product_data variable 
# #          product_data.append(product_dict) 
# #         
# #         
# #          # catching exception 
# #         
# #         except Exception as e:
# #              with open('exception.log', 'a+') as exception_file: 
# #         
# #          #logging errors with time of running 
# #                  exception_file.write( 
# #         'time: ' + str(datetime.datetime.now()) + '\n' + str(e) ) 
# #         
# #         with open('data.json', 'w') as file: 
# #         
# #          # writing data to the file 
# #         
# #          file.write(str(product_data))
# # =============================================================================
# 
# =============================================================================
