from flask import Flask, request, Response, render_template, jsonify
from random import shuffle
from functools import reduce
from utils.types import get_enum_ref
# Scrapers
from scrapers.scraper import Scraper
from scrapers.proxy import evaluate_proxies
from scrapers.jobs_builder import GoogleJobsScraper, IndeedScraper, MichaelPageScraper
# Contents
from contents.content import Content, get_contents_by_category, get_content_by_id, get_categories
# Surveys
from surveys.survey import Survey
from surveys.builder import get_survey, get_Checker
from surveys.db_survey import save_results, get_result
# Ai generator
import ai_generator
# Application
from config import config, load_environment
import sys

def init_variables():
    # Scrappers init proxy service
    evaluate_proxies()
    
    # Ai generator init api
    ai_generator.GEMINI_AI_SECRET_KEY = app.config['GEMINI_AI_SECRET_KEY']

def create_app(config_name):
    app.config.from_object(config[config_name])

    return app

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', app.config['ALLOW_SITES'])
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    return response

@app.errorhandler(404)
def page_not_found(self):
    return render_template("page-404.html")

########################################
# Auto test / Surveys routes
########################################

""" Get view of dynamic form
    Url params => 
        survey_name: form name
    
    return => html rendered
"""
@app.route("/formulario", methods=['GET'])
def get_survey_view():
    survey_name = request.args.get('survey_name')
    
    survey = get_survey(survey_name)
    
    if survey is None:
        return Response("{'error':'this survey namespace not exists'}", status=404, mimetype='application/json')
    
    survey_title = survey.get_survey_title(survey_name)
    
    total_questions = survey.get_total_questions()
    
    return jsonify(render_template("survey.html", API_URL=app.config['API_URL'], survey=survey, survey_title=survey_title, survey_name=get_enum_ref(survey_name, Survey.Type), survey_type=Survey.Type, question_behavior=Survey.Behavior, total_questions=total_questions)), 200

""" Get single result by event of survey
    Url params => 
        survey_name: form name

    Headers =>
        body: json dictionary
    
    return => html rendered
"""
@app.route("/formulario/respuesta", methods=['POST'])
def post_survey_response():
    survey_name = request.args.get('survey_name')
    data = request.get_json()

    checker = get_Checker(survey_name)

    response = checker.get_response(data)
    
    if response is None:
        return Response("{'error':'this survey not contain validation object'}", status=404, mimetype='application/json')
    
    response['total_score'] = reduce(lambda prev, next: prev + next, response.get('data', [0]))
    
    return jsonify(render_template("survey_results.html", response=response, survey_name=get_enum_ref(survey_name, Survey.Type), survey_type=Survey.Type)), 200

""" Get All user results of survey
    Url params => 
        id: id in database
    
    return => json dictionary
"""
@app.route("/formulario/resultados", methods=['GET'])
def get_survey_results():
    _id = request.args.get('id')
    
    result = get_result(_id)

    return result, 200

""" Post result of survey
    Url params => 
        survey_name: form name
        user_id: hash key

    Headers =>
        body: json dictionary
    
    return => _id
"""
@app.route("/formulario/resultado", methods=['POST'])
def post_survey_result():
    survey_name = request.args.get('survey_name')
    user_id = request.args.get('user_id')
    data = request.get_json()
    
    if data is None:
        return None, 400
    
    checker = get_Checker(survey_name)
    
    checker.validate(data)
    
    save_results(user_id=user_id, data=checker.get_results())
    
    return checker.get_results(), 200

########################################
# Suricatum multimedia contents routes
########################################

""" Get cards of category
    Url params => 
        type_content: content name
        category: category name
    
    return => html rendered
"""
@app.route("/contenido/lista", methods=['GET'])
def get_all_content():
    type_content = request.args.get('type_content')
    category = request.args.get('category')

    data = get_contents_by_category(type_content=type_content, selected_category=category)
    
    if data == []:
        return jsonify('Not found'), 404
    
    return jsonify(render_template("video_card.html", contents=data, type_enum=Content.Type, type_content=type_content)), 200

""" Get full content
    Url params => 
        restricted_content: boolean
        type_content: content name
        id: content original id
        
    return => html rendered
"""
@app.route("/contenido/solo", methods=['GET'])
def get_single_content():
    restricted_content = request.args.get('restricted_content')
    type_content = request.args.get('type_content')
    content_id = request.args.get('id')

    data = get_content_by_id(type_content=type_content, content_id=content_id)
    
    if data == None:
        return jsonify('Not found'), 404
    
    parameters = {
        "type_content" : type_content,
        "is_contain_default_cover" : data.is_contain_default_cover('thumbnails'),
        "restricted_content" : restricted_content
    }
    
    return jsonify(render_template("video_container.html", content=data, type_content=Content.Type, parameters=parameters)), 200

""" Get content category list
    Url params => 
        type_content: content name
        
    return => json dictionary
"""
@app.route("/contenido/categorias", methods=['GET'])
def get_content_categories():
    type_content = request.args.get('type_content')

    data = get_categories(type_content=type_content)
    
    if data == None:
        return jsonify('Not found'), 404
    
    return jsonify(data), 200

########################################
# Meta-Search Routes
########################################

""" Get card job offers to scrapers
    Url params => 
        job: charge + specialization 
        
    return => html rendered
"""
@app.route("/buscador-ofertas", methods=['GET'])
def get_scraper_response():
    job_name = request.args.get('jobname')

    google: Scraper = GoogleJobsScraper(job=job_name, url_params=[])
    indeed: Scraper = IndeedScraper(job=job_name)
    michael: Scraper = MichaelPageScraper(job=job_name)

    google.build_jobs()
    indeed.build_jobs()
    michael.build_jobs()

    job_list = google.get_jobs() + indeed.get_jobs() + michael.get_jobs()
    shuffle(job_list)
    if len(job_list) % 2 != 0:
        job_list.pop()
    
    data = { 'jobs_list' : job_list }
    return render_template("meta_search_results.html", data=data)

if __name__ == "__main__":
    env = 'production'
    if len(sys.argv) > 1 and sys.argv[1] == 'dev':
        env = 'development'
        load_environment(env)
        app = create_app(env)
        init_variables()
        app.run(port=25565)
    else:
        load_environment(env)
        app = create_app(env)
        init_variables()
        app.run()