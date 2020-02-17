#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
# Standard plotly imports
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from PIL import Image
import os
import io

import json

def read_data(data_path):
    data_file = open(data_path,encoding='utf-8-sig')
    data = json.loads(data_file.read())
    return data

reform = {'City':[],'Articles':[]}
data = read_data('poi_city.json')
data = sorted(data.items(), key=lambda d: d[1],reverse=True)

count = 0

for pair in data:
    reform['City'].append(pair[0])
    reform['Articles'].append(pair[1])
    count += pair[1]
df = pd.DataFrame.from_dict(reform)
print(count)

#df = pd.read_csv('route_cnt.csv')
#df = df.sort_values(by=['Route'],ascending=False)
#print(df)
fig = px.bar(df, x='City', y="Articles", barmode='group')
img_bytes = fig.to_image(format="png", width=800, height=400, scale=5)
image = Image.open(io.BytesIO(img_bytes))
image.save('city_articles.png')
