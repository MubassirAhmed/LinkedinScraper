# just run the spider in this file when you call main

import os

def executeSpider():

    os.system('cmd /c "cd ../ && scrapy crawl linkedin"')

def main():
    executeSpider()
