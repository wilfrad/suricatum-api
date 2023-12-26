import requests
import urllib.parse
from bs4 import BeautifulSoup
from scrapers.scraper import HEADERS, Job, Scraper

class IndeedScraper(Scraper):
    def __init__(self, job):
        if job != None:
            query = urllib.parse.quote(job)
            self.query_url = f'https://co.indeed.com/jobs?q={query}?'
        self.jobs = []
    
    def build_jobs(self, count = 0):
        res = requests.get(self.query_url, headers=HEADERS)
        if res.status_code == 200 or res.status_code == 301:
            soup = BeautifulSoup(res.text, 'html.parser')
            jobs_list = []
            job_cards = soup.find(id="mosaic-provider-jobcards").select('ul li')
            
            for item in job_cards:
                try:
                    post_link = 'https://co.indeed.com' + item.find('h2').find('a', href=True)['href']
                    title = item.find('h2').get_text(strip=True)
                    location = item.find(class_='location').get_text(strip=True) if item.find(class_='location') else None
                    salary = item.find(class_='salary').get_text(strip=True) if item.find(class_='salary') else None
                except TypeError:
                    print('item scraping error')
                try:
                    details = {
                        Job.JobDetail.SALARY: salary,
                    }

                    job_instance = Job(provider=Job.JobProvider.INDEED, post_link=post_link, title=title, location=location, details=details)
                    jobs_list.append(job_instance)
                except Exception as e:
                    print(f'build job error')
    
    def get_jobs():
        return self.jobs