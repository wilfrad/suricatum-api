from enum import Enum
from json import loads
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class Content:
    class Type(Enum):
        SURICATUM_TV = 'suricatum_tv'
        TESTIMONIALS = 'testimonials'

    def __init__(self, category, contents):

        self.category = category
        self.contents = contents

class Behavior:
    """ If date_str is Date format, return days since date
        if is not format, return same
    """
    def get_days_since_date(self, date_str):

        try:
            new_date = datetime.strptime(date_str, '%Y/%m/%d')
            return f"Hace {(datetime.now() - new_date).days} dias"
        except (TypeError, ValueError):
            return date_str

    """ Divide url cover validate 
        if contained target in route
    """ 
    def is_contain_default_cover(self, target):
        components_url = urlparse(self.images.content_cover)

        route = components_url.path
        
        print(self.images.content_cover)
        
        return #target in route.split('/')

    def unique_id(self):

        unique_str = f"{self.tag}-{self.content_title}-{self.content_url}"
        return hash(unique_str)

class Thumbnails:

    def __init__(self, content_thumbnail = None, content_cover = None, profile_photo = None, brand_logotype = None):

        self.content_thumbnail = content_thumbnail
        self.content_cover = content_cover
        self.profile_photo = profile_photo
        self.brand_logotype = brand_logotype

class TestimonialContent(Behavior):

    def __init__(self, images, main_header, tag, profile_url, content_title, content_url):

        self.images = Thumbnails(**images)
        self.main_header = main_header
        self.tag = tag
        self.profile_url = profile_url
        self.content_title = content_title
        self.content_url = content_url
        self.id = content_url


class SuricatumTvContent(Behavior):

    def __init__(self, images, tag, content_title, content_url):

        self.images = Thumbnails(**images)
        self.tag = self.get_days_since_date(tag)
        self.content_title = content_title
        self.content_url = content_url
        self.id = content_url

TESTIMONIALS_CONTENT = None
SURICATUM_TV_CONTENT = None

def init_builder():

    global TESTIMONIALS_CONTENT
    global SURICATUM_TV_CONTENT
    if TESTIMONIALS_CONTENT is None or SURICATUM_TV_CONTENT is None: 
        if TESTIMONIALS_CONTENT is None:
            with open("app/contents/data/testismonials.json", "r", encoding='utf-8') as file:
                TESTIMONIALS_CONTENT = file.read()
        
        if SURICATUM_TV_CONTENT is None:
            with open("app/contents/data/suricatum_tv.json", "r", encoding='utf-8') as file:
                SURICATUM_TV_CONTENT = file.read()

def get_contents_by_category(type_content, selected_category):

    init_builder()
    
    data_list = None
    if type_content == Content.Type.SURICATUM_TV.value:
        data_list = loads(SURICATUM_TV_CONTENT)
    elif type_content == Content.Type.TESTIMONIALS.value:
        data_list = loads(TESTIMONIALS_CONTENT)
    else:
        return []
    
    result = []
    for item in data_list:
        category = item['category']
        contents = item['contents']

        if category['id'] == selected_category:
            content_list = []
            for data in contents:
                content = None
                if type_content == Content.Type.SURICATUM_TV.value:
                    content = SuricatumTvContent(**data)
                
                if type_content == Content.Type.TESTIMONIALS.value:
                    content = TestimonialContent(**data)
                
                content_list.append(content)
                
            result = content_list

    return result

def get_content_by_id(type_content, content_id):

    init_builder()
    
    data_list = None
    if type_content == Content.Type.SURICATUM_TV.value:
        data_list = loads(SURICATUM_TV_CONTENT)
    elif type_content == Content.Type.TESTIMONIALS.value:
        data_list = loads(TESTIMONIALS_CONTENT)
    else:
        return None

    for item in data_list:
        contents = item['contents']
        
        for data in contents:
            content = None
            if type_content == Content.Type.SURICATUM_TV.value:
                content = SuricatumTvContent(**data)
            
            if type_content == Content.Type.TESTIMONIALS.value:
                content = TestimonialContent(**data)
            
            if content.id == content_id:
                return content
    
    return None

def get_categories(type_content):
    
    init_builder()
    
    data_list = None
    if type_content == Content.Type.SURICATUM_TV.value:
        data_list = loads(SURICATUM_TV_CONTENT)
    elif type_content == Content.Type.TESTIMONIALS.value:
        data_list = loads(TESTIMONIALS_CONTENT)
    else:
        return None
        
    categories = {}
    for item in data_list:
        categories[item['category']['id']] = item['category']['display_name']
    
    return categories