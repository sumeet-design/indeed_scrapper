from django.shortcuts import render
from django.http import HttpResponse
from myscrapper.models import Job  # Import your Job model
import pymongo
from django.conf import settings

# Parsing and creating xml data
from lxml import etree as et
import pymongo
# Store data as a csv file written out
from csv import writer

# In general to use with timing our function calls to Indeed
import time

# Assist with creating incremental timing for our scraping to seem more human
from time import sleep

# # Dataframe stuff
# import pandas as pd

# Random integer for more realistic timing for clicks, buttons and searches during scraping
from random import randint

# Multi Threading
import threading

# Threading:
from concurrent.futures import ThreadPoolExecutor, wait

import selenium

# import aiohttp

import asyncio

# Check version I am running
selenium.__version__
from selenium import webdriver

# Starting/Stopping Driver: can specify ports or location but not remote access
from selenium.webdriver.chrome.service import Service as ChromeService

# Manages Binaries needed for WebDriver without installing anything directly
from webdriver_manager.chrome import ChromeDriverManager

# Allows searchs similar to beautiful soup: find_all
from selenium.webdriver.common.by import By

# Try to establish wait times for the page to load
from selenium.webdriver.support.ui import WebDriverWait

# Wait for specific condition based on defined task: web elements, boolean are examples
from selenium.webdriver.support import expected_conditions as EC

# Used for keyboard movements, up/down, left/right,delete, etc
from selenium.webdriver.common.keys import Keys

# Locate elements on page and throw error if they do not exist
from selenium.common.exceptions import NoSuchElementException


def scrape_and_store_data(request):
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['indeed']
    collection = db['myscrapper_job']

   


    option= webdriver.ChromeOptions()

    # Going undercover:
    # option.add_argument("--incognito")
    # option.add_argument("--headless=new")

    # Finding location, position, radius=35 miles, sort by date and starting page
    paginaton_url = 'https://in.indeed.com/jobs?q={}&l={}&radius=35&filter=0&sort=date&start={}'
    print("this is pagination",paginaton_url)
    start = time.time()




    job_='Python+developer'
    location=''

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                            options=option)


    driver.get(paginaton_url.format(job_,location,0))

    # t = ScrapeThread(url_)
    # t.start()

    sleep(randint(2, 6))

    p=driver.find_element(By.CLASS_NAME,'jobsearch-JobCountAndSortPane-jobCount').text

    # Max number of pages for this search! There is a caveat described soon
    max_iter_pgs=int(p.split(' ')[0].replace(',',''))//15 


    driver.quit() # Closing the browser we opened


    end = time.time()

    print(end - start,'seconds to complete action!')
    print('-----------------------')
    print('Max Iterable Pages for this search:',max_iter_pgs)




    start = time.time()


    # job_='Data+Engineer'
    # location='Washington'


    job_list=[]
    job_description_list_href=[]

    # job_description_list = []
    salary_list=[]


    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                            options=option)
    sleep(randint(2, 6))

    # driver.get("https://www.indeed.com/q-USA-jobs.html")

    for i in range(0,3):
        driver.get(paginaton_url.format(job_,location,i*10))
        
        
        sleep(randint(2, 4))

        job_page = driver.find_element(By.ID,"mosaic-jobResults")
        jobs = job_page.find_elements(By.CLASS_NAME,"job_seen_beacon") # return a list

        for jj in jobs:
            job_title = jj.find_element(By.CLASS_NAME,"jobTitle")
    #         print(job_title.text)
            # Add job details to the job_list
            job_list.append({
                'title': job_title.text,
                'href': job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("href"),
                'id': job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("id"),
                'company': jj.find_element(By.CLASS_NAME, "companyName").text,
                'location': jj.find_element(By.CLASS_NAME, "companyLocation").text,
                'date': jj.find_element(By.CLASS_NAME, "date").text,
                'href_full': job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            })

            try:
                salary_list.append(jj.find_element(By.CLASS_NAME, "salary-snippet-container").text)
            except NoSuchElementException:
                try:
                    salary_list.append(jj.find_element(By.CLASS_NAME, "estimated-salary").text)
                except NoSuchElementException:
                    salary_list.append(None)

    # Loop through the scraped data and store it in MongoDB and your Django model
    count = -1
    for job_data in job_list:
        count = count + 1
        job = Job(
            title=job_data['title'],
            href=job_data['href'],
            company=job_data['company'],
            location=job_data['location'],
            date=job_data['date'],
            href_full=job_data['href_full'],
            salary=salary_list[count]
        )
        job.save()


        # Store data in MongoDB
        # document = {
        #     'title': job_data['title'],
        #     'href': job_data['href'],
        #     'company': job_data['company'],
        #     'location': job_data['location'],
        #     'date': job_data['date'],
        #     'href_full': job_data['href_full'],
        #     'salary': salary_list[i]
        # }
        # collection.insert_one(document)

    # Close the MongoDB connection
    client.close()

    return HttpResponse("Data scraped and stored successfully!")

