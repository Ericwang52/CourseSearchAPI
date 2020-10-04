import flask
import bs4
import requests
import selenium
import sys, time
import re
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
    finaldict= {"edx":scrapedx(term, sale, 4, driver), "Udemy":scrapUdemy(term, sale, 4, driver), "Coursera":scrapCoursera(term, sale, 4, driver)}
    return jsonify(finaldict)

def scrapedx(term, sale, minrate, driver):
    link = "https://www.edx.org/search?q="+term
    driver.get(link)
    time.sleep(2)
    pbutton=driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/div/div[2]/div/div[1]/div[1]/div/button')
    pbutton.click()
    time.sleep(2)

    html_content=driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    courses= soup.find_all("div", {"class": "discovery-card-inner-wrapper"})
    if courses is None:
        return
    org="edx"

    finaldict={}
    for i in range(len(courses)):
        name=courses[i]["aria-label"]
        provider=str(courses[i].find("div", {"class":"provider"}).findAll()[1].span.span.contents[0])
        url="https://edx.org"+ courses[i].a["href"]
        course={"name":name, "provider":provider, "url":url}
        finaldict[i]=course

    return finaldict
def scrapUdemy(term, sale, minrate, driver):
    link = "https://www.udemy.com/courses/search/?q=" + term
   # driver.implicitly_wait(10)

    driver.get(link)
    time.sleep(5)
    html_content=driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    courses=soup.find_all("a", {"query": True})
    if courses is None:
        return
    finaldict={}
    #searchterm= soup.find("h1", {"class": "udlite-heading-xxl"}).split("for",1)[1] 
    org="Udemy"
    for i in range(len(courses)):
        name=courses[i].div.find("div",{"class":"udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE"}).contents[0]
        provider=courses[i].find("div", {"data-purpose": "safely-set-inner-html:course-card:visible-instructors"}).contents[0]
        url="https://udemy.com"+ courses[i]["href"]
        rating= str(courses[i].find("span", {"data-purpose": "rating-number"}).contents[0])
        if courses[i].find("div",{"data-purpose":"original-price-container"}) is not None:
            price=str(courses[i].find("div",{"data-purpose":"original-price-container"}).div.findAll()[1].span.contents[0])
        else:
             price=str(courses[i].find("div",{"data-purpose":"course-price-text"}).findAll()[1].span.contents[0])
        course={"name":name, "provider":provider, "url":url, "rating": rating, "price": price}
        finaldict[i]=course
    return finaldict

def scrapCoursera(term, sale, minrate, driver):
    link = "https://www.coursera.org/search?query="+term
    driver.get(link)
    html_content=driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    courses= soup.find_all("li", {"class": "ais-InfiniteHits-item"})
    if courses is None:
        return
    org="Coursera"
    finaldict={}
    for i in range(len(courses)):
        name=courses[i].find("h2", {"class": "color-primary-text card-title headline-1-text"}).contents[0]
        provider=str(courses[i].find("span", {"class":"partner-name"}).contents[0])
        url="https://coursera.org"+ courses[i].div.a["href"]
        rating=courses[i].find("span", {"class":"ratings-text"}).contents[0]
        course={"name":name, "provider":provider, "url":url, "rating": rating}
        finaldict[i]=course
    return finaldict




app.run()