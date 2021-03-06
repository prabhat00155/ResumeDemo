﻿import urllib.request
import json
from random import randint
import sys
import gzip
from bs4 import BeautifulSoup

def getValues(tag, hook, subtag, parsed_data):
	result = ""
	try:
		parsed_data = parsed_data.findAll(tag, {hook: subtag}) 
		parsed_data = BeautifulSoup(str(parsed_data), "html.parser")
		result = parsed_data.get_text(" ")
	except:
		pass 
	return result
	
def getHTML(handle):
    url = "https://www.linkedin.com/in/" + handle
    PROXIES = ["http://flower:123ai@45.33.152.66:80", "http://flower:107.173.177.148:80", "http://flower:45.33.152.193:80", "http://flower:107.174.140.245:80", "http://flower:107.175.1.69:80"]

    proxies = {"https":PROXIES[randint(0, 4)]}
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36", "accept-encoding": "gzip, deflate, sdch, br", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    req = urllib.request.Request(url, headers=headers)
    parsed_html = ""
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        obj = gzip.decompress(result)
        #print(obj)
        parsed_html = BeautifulSoup(obj, "html.parser")
        #print(parsed_html)
    
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
    return parsed_html

def getData(parsed_html, handle):
    returnData = {}
    url = "https://www.linkedin.com/in/" + handle
    returnData["url"] = url
    name = ""
    headline = ""
    connections = ""
    try:
        name = parsed_html.title.string.split("|")[0] #Title
        headline = parsed_html.p.string #Headline
        connections = str(parsed_html.findAll("div", {"class" : "member-connections"})[0]).split(">")[2].split("<")[0]
    except:
        pass
    returnData["name"] = name
    returnData["headline"] = headline
    returnData["connections"] = connections
    skills = ""
    try:
        skills = getValues("section", "id", "skills", parsed_html)
        if skills != "":
            skills = skills.split("See less")[0].split("Skills")[1]
    except:
        pass
    returnData["skills"] = skills	
    
    schools = parsed_html.findAll("li", {"class" : "school"})
    parsed_schools = BeautifulSoup(str(schools), "html.parser")
    schools = getValues("h4", "class", "item-title", parsed_schools)
    returnData["schools"] = schools
    
    experience = parsed_html.findAll("section", {"id" : "experience"})
    parsed_experience = BeautifulSoup(str(experience), "html.parser")
    roles = getValues("h4", "class", "item-title", parsed_experience)
    returnData["roles"] = roles
    companies = getValues("h5", "class", "item-subtitle", parsed_experience)
    returnData["companies"] = companies
    
    summary = getValues("p", "class", "description", parsed_experience)
    returnData["summary"] = summary
    
    industry = parsed_html.findAll("dl", {"id" : "demographics"})
    parsed_industry = BeautifulSoup(str(industry), "html.parser")
    industry = getValues("dd", "class", "descriptor adr", parsed_industry)
    returnData["industry"] = industry

    return returnData