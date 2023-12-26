from abc import ABC, abstractmethod
from enum import Enum

HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}

class Scraper(ABC):
    @abstractmethod
    def build_jobs(self, soup, count = 0):
        pass
    
    @abstractmethod
    def get_jobs(self):
        pass

class Job:
    class JobDetail(Enum):
        SALARY = 'salary'
        LOCATION = 'location'
        POST_DATE = 'post_date'
        HORARY = 'horary'
        CONTRACT_TYPE = 'contract_type'
        NATURE = 'nature'

    class JobProvider(Enum):
        GOOGLE_JOBS = 'Google Jobs'
        MICHAELPAGE = 'Michaelpage.com'
        JOBZEM = 'Jobzem'
        JOBTED = 'Jobted'
        INDEED = 'Indeed'
        JOBLEADS = 'Jobleads'
        LINKEDIN_JOBS = 'Linkedin Jobs'
        JOBRAPIDO = 'Jobrapido'

    def __init__(self, provider, post_link, title, location, details):
        self.provider = provider
        self.post_link = post_link
        self.title = title
        self.location = location
        self.details = details
