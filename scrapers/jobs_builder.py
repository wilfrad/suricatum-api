import requests
import urllib.parse
from bs4 import BeautifulSoup
from scrapers.scraper import Job, Scraper
from scrapers.proxy import proxy_request

class GoogleJobsScraper(Scraper):
    def __init__(self, job, url_params):
        if job:
            self.job = urllib.parse.quote(job)
        self.url_params = url_params
        self.jobs = []
        self.__build_url_request()

    def __build_url_request(self):
        base_url = f'https://www.google.com/search?q={self.job}&ibp=htl;jobs&htichips='
        
        params = ''
        if False:
            for key, value in self.url_params.items():
                if value != None:
                    params += f'{key}={value}' + ','
        
        self.base_url = base_url + params[:-1]

    def build_jobs(self, count = 0):
        res = proxy_request(self.base_url)

        if res is None:
            return []

        if res.status_code == 200 or res.status_code == 301:
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
                    job_instance = Job(provider=Job.JobProvider.GOOGLE_JOBS, post_link=post_link, title=title, location=location, details=details)
                    jobs_list.append(job_instance)
                except:
                    print('build job error')
            
            self.jobs = jobs_list

    def get_jobs(self):
        return self.jobs

class IndeedScraper(Scraper):
    def __init__(self, job):
        if job != None:
            query = urllib.parse.quote(job)
            self.query_url = f'https://co.indeed.com/jobs?q={query}?'
        self.jobs = []
    
    def build_jobs(self, count = 0):
        res = proxy_request(self.query_url)

        if res is None:
            return []

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
    
    def get_jobs(self):
        return self.jobs

class MichaelPageScraper(Scraper):
    def __init__(self, job):
        if job != None:
            query = urllib.parse.quote(job)
            self.query_url = f'https://www.michaelpage.com.co/jobs/{query}?'
        self.jobs = []

    def build_jobs(self, count = 0):
        res = proxy_request(self.query_url)

        if res is None:
            return []
        
        if res.status_code == 200 or res.status_code == 301:
            soup = BeautifulSoup(res.text, 'html.parser')

            jobs_items = soup.select('.view-content li.views-row')

            jobs_list = []
            base_url = 'https://www.michaelpage.com.co'
            for item in jobs_items:
                try:
                    post_link = f"{base_url}{item.select_one('.view-job')['href']}"
                    title = item.select_one('.job-title h3 a').text.strip()
                    location = item.select_one('.job-location').text.strip()
                    salary = item.select_one('.job-salary').text.strip() if item.select_one('.job-salary') else None
                    contract_type = item.select_one('.job-contract-type').text.strip() if item.select_one('.job-contract-type') else None
                    nature = item.select_one('.job-nature').text.strip() if item.select_one('.job-nature') else None
                except TypeError:
                    print('item scraping error')
                try:
                    details = {
                        Job.JobDetail.SALARY : salary,
                        Job.JobDetail.CONTRACT_TYPE : contract_type,
                        Job.JobDetail.NATURE : nature
                    }
                    job_instance = Job(provider=Job.JobProvider.MICHAELPAGE, post_link=post_link, title=title, location=location, details=details)
                    jobs_list.append(job_instance)
                except Exception:
                    print('build job error')

            self.jobs = jobs_list

    def get_jobs(self):
        return self.jobs