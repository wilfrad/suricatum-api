import requests
from bs4 import BeautifulSoup

url='https://www.google.com/search?q=gerente+administrativo+bogota&ibp=htl;jobs#htivrt=jobsfpstate=tldetail'
headers={'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}

res = requests.get(url, headers=headers) 

soup = BeautifulSoup(res.text, 'html.parser') 

class Job:
    def __init__(self, title, location, publish_date, horary):
        self.title = title
        self.location = location
        self.publish_date = publish_date
        self.horary = horary

def build_jobs():
    jobs_list = []
    for job in soup.findAll(attrs={'jsname' : 'DVpPy'}):
        try:
            title = job.find(class_='BjJfJf').get_text().strip()
            location = job.find(class_='vNEEBe').get_text().strip()
            
            details = job.findAll(class_='LL4CDc')
            if len(details) > 1:
                publish_date = details[0].get_text().strip()
                horary = details[1].get_text().strip()
            else:
                horary = details[0].get_text().strip()
            
            print(title,'\n    Compañía/lugar: ', location,'\n    Publicación: ', publish_date,'\n    Horario: ', horary)
            
            job_obj = Job(title=title, location=location, publish_date=publish_date, horary=horary)
            jobs_list.append(job_obj)
        except TypeError as ex:
            print(str(ex))
    
    return jobs_list

def scrape_job(job):
    return ''

def get_job_details(job):
    return ''

build_jobs()