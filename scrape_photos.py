import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pprint as pp


def get_photo_info():
    data = pd.read_csv("data/tag_links.csv")
    result=[]
    
    for i in range(len(data)):
        if i % 100 == 0:
            print("{}%".format(round(i*100/len(data), 2)))
        
        try:
            page = urlopen(data["link"][i]).read()
            data_new = bs(page, 'html.parser')
            script = data_new.find('body').find('script')
            raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
            json_data=json.loads(raw)
            posts =json_data['entry_data']['PostPage'][0]['graphql']
            x = {"tag": data["tag"][i],
                "url": posts['shortcode_media']['display_resources'][0]['src'],
                "height": posts['shortcode_media']['dimensions']['height'],
                "width": posts['shortcode_media']['dimensions']['width'],
                "config_height": posts['shortcode_media']['display_resources'][0]['config_height'],
                "config_width": posts['shortcode_media']['display_resources'][0]['config_width'],
                }
            try:
                x["related_words"] = posts['shortcode_media']['accessibility_caption']
            except:
                x["related_words"] = None
            
            result.append(x)
            
        
        except Exception as e:
            print("Failed")
            print(e)
            
        
    
    return pd.DataFrame(result)

if __name__ == "__main__":
    photo_data = get_photo_info()
    print(len(photo_data))
    print("Finished")
    photo_data.to_csv("data/photo_info.csv")
