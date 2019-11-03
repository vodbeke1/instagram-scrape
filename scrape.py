import requests
import pprint
import os
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
from dotenv import load_dotenv

from pathlib import Path
env_path = Path(".") / "env/.env"
load_dotenv(dotenv_path=env_path)


tags = pd.read_csv("data/tags.csv")

CHROME_DRIVER = os.getenv("CHROME_DRIVER")

links = []
tag_links = []
counter = 0
browser = webdriver.Chrome(executable_path=CHROME_DRIVER)

for hashtag in tags["tag"].head(20):
    print(hashtag)
    
    
    browser.get('https://www.instagram.com/explore/tags/'+hashtag)
    Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight/1.5);")
    source = browser.page_source
    data=bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')
    try:
        for link in script.findAll('a'):
            if re.match("/p", link.get('href')):
                links.append('https://www.instagram.com'+link.get('href'))
                tag_links.append(hashtag)
    except:
        "Tag was passed"


    for i in range(3):
        time.sleep(2)
        Pagelength = browser.execute_script("window.scrollTo(document.body.scrollHeight/{}, document.body.scrollHeight/{});".format(1.5*(i+1), 1.5*(i+1)+1.5))
        source = browser.page_source
        data=bs(source, 'html.parser')
        body = data.find('body')
        script = body.find('span')
        try:
            for link in script.findAll('a'):
                if re.match("/p", link.get('href')):
                    links.append('https://www.instagram.com'+link.get('href'))
                    tag_links.append(hashtag)
        except:
            pass
    #browser.close()

pd.DataFrame({"tag": tag_links, "link": links}).to_csv("data/tag_links.csv")






