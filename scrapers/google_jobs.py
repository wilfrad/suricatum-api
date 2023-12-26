import requests
import urllib.parse
from bs4 import BeautifulSoup
from scrapers.scraper import HEADERS, Job, Scraper

class GoogleJobsScraper(Scraper):
    def __init__(self, job, url_params):
        if job != None:
            self.job = urllib.parse.quote(job)
        self.url_params = url_params
        self.jobs = []
        
        self.__build_url_request()

    def __build_url_request(self):
        base_url = f'https://www.google.com/search?q={self.job}&ibp=htl;jobs&htichips='
        
        params = ''
        for key, value in self.url_params.items():
            if value != None:
                params += f'{key}={value}' + ','
        
        self.base_url = base_url + params[:-1]

    def build_jobs(self, count = 0):
        res = requests.get(self.base_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        jobs_items = soup.select('ul li')

        jobs_list = []
        for item in jobs_items:
            job_instance = ''
            try:
                post_link = item.find(attrs={'data-share-url': True})['data-share-url']

                title = item.select_one('.BjJfJf.PUpOsf').text.strip()

                location = item.select_one('.Qk80Jf').text.strip()

                salary = None
                salary_icon = item.select_one('.z1asCe.iQPETc')
                if salary_icon:
                    salary = salary_icon.find_next('span').text.strip()

                post_date = None
                post_date_icon = item.select_one('.z1asCe.EZMfad')
                if post_date_icon:
                    post_date = post_date_icon.find_next('span').text.strip()

                horary = None
                horary_icon = item.select_one('.z1asCe.mQ5pwc')
                if horary_icon:
                    horary = horary_icon.find_next('span').text.strip()

            except TypeError:
                print('item scraping error')
            try:
                details = {
                    Job.JobDetail.SALARY : salary,
                    Job.JobDetail.POST_DATE : post_date,
                    Job.JobDetail.HORARY : horary
                }
                job_instance = Job(post_link=post_link, title=title, location=location, details=details)
                jobs_list.append(job_instance)
            except:
                print('build job error')
        
        self.jobs = jobs_list

    def get_jobs(self):
        return self.jobs