import flask
import bs4
import requests
import selenium
from selenium import webdriver
from flask import request, jsonify
from bs4 import BeautifulSoup # HTML data structure
from urllib.request import urlopen as uReq  # Web client


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/search', methods=['GET'])
def search():
    if 'term' in request.args:
        term = str(request.args['term'])
    else:
        return "Error: No term field provided. Please specify an id."
    if 'sale' in request.args:
        sale = (request.args['sale'])
    else:
        return "Error: No term field provided. Please specify an id."
    return scrapedx(term, sale, 4)

def scrapedx(term, sale, minrate):
    link = f"https://www.edx.org/search?q={term}"
    driver = webdriver.PhantomJS(executable_path='/Applications/phantomjs-2.1.1-macosx/bin/phantomjs')
    driver.get(link)
    html_content=driver.page_source
    soup = BeautifulSoup(html_content, "lxml")
    return html_content


app.run()