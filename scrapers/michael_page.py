import requests
import urllib.parse
from bs4 import BeautifulSoup
from scraper import HEADERS, Job, Scraper

class MichaelPageScraper(Scraper):
    def __init__(self, job):
        if job != None:
            query = urllib.parse.quote(job)
            self.query_url = f'https://www.michaelpage.com.co/jobs/{query}?'
        self.jobs = []

    def build_jobs(self, count = 0):
        res = requests.get(self.query_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')

        jobs_items = soup.select('.view-content li.views-row')

        jobs_list = []
        base_url = 'www.michaelpage.com'
        for item in jobs_items:
            try:
                post_link = base_url + item.select_one('.view-job')['href']
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
                job_instance = Job(post_link=post_link, title=title, location=location, details=details)
                jobs_list.append(job_instance)
            except Exception:
                print('build job error')

        self.jobs = jobs_list

    def get_jobs(self):
        return self.jobs

jobs_list = MichaelPageScraper('contador').build_jobs()
for job in jobs_list:
    print(f"Title: {job.title},\n Location: {job.location},\n Salary: {job.details.get('salary')},\n Contract Type: {job.details.get('contract_type')},\n Nature: {job.details.get('nature')},\n Post Link: {job.post_link}")
    print('-------------------------------------------')