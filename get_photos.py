import os
import requests
import pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import urllib.request
import io
import binascii
from PIL import Image
from io import BytesIO
import time

result = pd.read_csv("data/photo_info.csv")
directory="data/photos/"

    
def scrape():
    for i in result.index:
        time.sleep(1)
        if i > 1000:
            break
        r = requests.get(result.iloc[i]["url"])

        # create image from binary content
        """
        img = Image.open(BytesIO(r.content))

        width, height = img.size
        img = img.resize((100,100))
        """

        with open("{}{}-{}.jpg".format(directory, i, result["tag"][i]), 'wb') as f:
            f.write(r.content)
        
if __name__ == "__main__":
    scrape()
    