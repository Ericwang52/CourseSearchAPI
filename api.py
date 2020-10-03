import flask
import bs4
import requests
import selenium
import sys, time
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
        term = (request.args['term'])
    else:
        return "Error: No term field provided. Please specify an id."
    if 'sale' in request.args:
        sale = (request.args['sale'])
    else:
        return "Error: No term field provided. Please specify an id."
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    return scrapUdemy(term, sale, 4, driver)

def scrapedx(term, sale, minrate, driver):
    link = "https://www.edx.org/search?q="+term
    driver.get(link)
    html_content=driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    courses= soup.find_all("div", {"class": "discovery-card Verified and Audit col col-xl-3 mb-4 scrollable-discovery-card-spacing"})
    org="edx"
    finaldict={}
    for i in range(len(courses)):
        name=courses[i]["aria-label"]
        provider=str(courses[i].find("span", {"width":"220"}).span.span.contents[0])
        url="https://edx.org"+ courses[i].a["href"]
        course={"org":org,"name":name, "provider":provider, "url":url}
        finaldict[i]=course

    return jsonify(finaldict)
def scrapUdemy(term, sale, minrate, driver):
    link = "https://www.udemy.com/courses/search/?q=" + term
   # driver.implicitly_wait(10)

    driver.get(link)
    time.sleep(5)
    html_content=driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    courses=soup.find_all("a", {"query": term.lower()})
    finaldict={}
    org="udemy"
    for i in range(len(courses)):
        name=courses[i].div.find("div",{"class":"udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE"}).contents[0]
        provider=courses[i].find("div", {"data-purpose": "safely-set-inner-html:course-card:visible-instructors"}).contents[0]
        url="https://edx.org"+ courses[i]["href"]
        price=
        rating=
        course={"org":org,"name":name, "provider":provider, "url":url}
        finaldict[i]=course
    return html_content




app.run()