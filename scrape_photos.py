import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen


def get_photo_info():
    data = pd.read_csv("data/tag_links.csv")
    links = data["link"]
    tag = data["tag"] 
    result=pd.DataFrame()
    tag_ = []

    for i in range(len(links)):
        try:
            page = urlopen(links[i]).read()
            data = bs(page, 'html.parser')
            script = data.find('body').find('script')
            raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
            json_data=json.loads(raw)
            posts =json_data['entry_data']['PostPage'][0]['graphql']
            x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
            x.columns =  x.columns.str.replace("shortcode_media.", "")
            result.append(x)
            tag_.append(tag[i])
            print("Success")

        except:
            print("Failed")
    result["tag"] = tag_

    # Just check for the duplicates
    result = result.drop_duplicates(subset = 'shortcode')
    result.index = range(len(result.index))
    return result

if __name__ == "__main__":
    photo_data = get_photo_info()
    print(len(photo_data))
    photo_data.to_csv("data/photo_info.csv")
