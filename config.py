import os
from dotenv import load_dotenv

class Config:
    API_URL = os.getenv('API_URL')
    GEMINI_AI_SECRET_KEY = os.getenv('GEMINI_AI_SECRET_KEY')
    ALLOW_ORIGIN = os.getenv('ALLOW_ORIGIN')
    DEBUG = os.getenv('FLASK_DEBUG', default=False)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}

def load_environment(env):
    if env == 'development':
        path = 'app/.env.development'
    else:
        path = 'app/.env.production'
    load_dotenv(dotenv_path=path)