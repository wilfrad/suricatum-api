import urllib
from flask import Flask, request, render_template, jsonify
from random import shuffle
from scrapers.scraper import Scraper
from scrapers.jobs_scraper import GoogleJobsScraper, MichaelPageScraper

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    return response

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page-404.html")

@app.route("/")
def get_scraper_response(methods=['GET']):
    job_name = request.args.get('jobname')

    google: Scraper = GoogleJobsScraper(job=job_name)
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