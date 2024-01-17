from flask import Flask, request, render_template, jsonify
from random import shuffle
from scrapers.scraper import Scraper
from scrapers.jobs_scraper import GoogleJobsScraper, MichaelPageScraper
from contents.content import Content, get_contents_by_category, get_content_by_id, get_categories

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

@app.errorhandler(404)
def page_not_found(self):
    return render_template("page-404.html")

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
        type_content: content name
        id: content original id
        
    return => html rendered
"""
@app.route("/contenido/solo", methods=['GET'])
def get_single_content():
    type_content = request.args.get('type_content')
    content_id = request.args.get('id')

    data = get_content_by_id(type_content=type_content, content_id=content_id)
    
    if data == None:
        return jsonify('Not found'), 404
    
    return jsonify(render_template("video_container.html", content=data, type_enum=Content.Type, type_content=type_content)), 200

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
    michael: Scraper = MichaelPageScraper(job=job_name)

    google.build_jobs()
    michael.build_jobs()

    job_list = google.get_jobs() + michael.get_jobs()
    shuffle(job_list)
    if len(job_list) % 2 != 0:
        job_list.pop()
    data = { 'jobs_list' : job_list }
    return jsonify(render_template("index.html", data=data))

if __name__ == "__main__":
    app.run(debug=True, port=25565)