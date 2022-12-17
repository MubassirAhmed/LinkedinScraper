# just run the spider in this file when you call main
#? TODO
#? log the errors from the scraper, and the 'INFO'
import os
from datetime import datetime


def executeSpider(*args):
    feed_settings = f"FEEDS = {{\"s3://linkedin-scraper-1/linkedin/{args[0]}\": {{\"format\": \"csv\"}} }}"
    cmd = f'ulimit -n 2048 && cd ~/Cool\ Stuff/LinkedInScraper/linkedin/ && scrapy crawl tester -s {feed_settings}'
    os.system(cmd)

def main():
    s3FileName = datetime.now().strftime('%Y-%m-%d_Time-%H-%M{}'.format('.csv'))
    executeSpider(s3FileName)
    
    return s3FileName

"""def test(*args):
    return f"FEEDS = {{\"s3://linkedin-scraper-1/linkedin/{args[0]}\": {{\"format\": \"csv\"}} }}"

if __name__ == "__main__":
    s3FileName = datetime.now().strftime('%Y-%m-%d_Time-%H-%M{}'.format('.csv'))
    print(test(s3FileName))"""