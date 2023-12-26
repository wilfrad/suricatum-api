import requests
from bs4 import BeautifulSoup

url='https://www.google.com/search?q=gerente+administrativo+bogota&ibp=htl;jobs#htivrt=jobsfpstate=tldetail'
headers={'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

class Job:
    def __init__(self, post_id, title, location, salary='', post_date='', horary=''):
        self.post_id = post_id
        self.title = title
        self.location = location
        self.salary = salary
        self.post_date = post_date
        self.horary = horary

def build_jobs():
    job_items = soup.select('ul li')

    jobs_list = []
    for item in job_items:
        post_id = item.find(attrs={'data-share-url': True})['data-share-url']

        title = item.select_one('.BjJfJf.PUpOsf').text.strip()

        location = item.select_one('.Qk80Jf').text.strip()

        salary = ''
        salary_icon = item.select_one('.z1asCe.iQPETc')
        if salary_icon:
            salary = salary_icon.find_next('span').text.strip()

        post_date = ''
        post_date_icon = item.select_one('.z1asCe.EZMfad')
        if post_date_icon:
            post_date = post_date_icon.find_next('span').text.strip()

        horary = ''
        horary_icon = item.select_one('.z1asCe.mQ5pwc')
        if horary_icon:
            horary = horary_icon.find_next('span').text.strip()

        job_instance = Job(post_id, title, location, salary, post_date, horary)
        jobs_list.append(job_instance)

for job in build_jobs():
    print(vars(job))