from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

HASHTAG_URL = "https://top-hashtags.com/instagram/"
r = requests.post(url=HASHTAG_URL)

soup = bs(r.text, features="html.parser")
links = soup.find_all("a")

tags = []
for i in links:
    _str_ = i.get("href")
    if "/hashtag/" in _str_:
        _, _, word, _ = _str_.split("/")
        tags.append(word)

pd.DataFrame({"tag": tags}).to_csv("data/tags.csv")