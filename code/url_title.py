from data_extractor import PixnetArticle
from operator import itemgetter
import json

data_gen = PixnetArticle()

title_dict = {}
count = 0 
for data_str in data_gen:
    count += 1
print(count)
    #data = json.loads(data_str)
    #title_dict[data['url']] = data['title']
#print(title_dict)

#with open('WebAPI/url_title.json', 'w') as outfile:
#    json.dump(title_dict, outfile,ensure_ascii=False)
