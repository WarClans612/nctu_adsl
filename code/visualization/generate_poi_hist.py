import json

#Source data path configuration
districts_data_path = '/home/pixnet/code/poi_data/taiwan_districts_mapping.json'
poi_addr_data_path = '/home/pixnet/code/poi_data/location_POIs.json'
article_poi_data_path = '/home/pixnet/code/poi_data/article2POIlist.json'


def read_data(data_path):
    data_file = open(data_path,encoding='utf-8-sig')
    data = json.loads(data_file.read())
    return data

poi_location_data = read_data(poi_addr_data_path)
article_poi_data = read_data(article_poi_data_path)

result = {}

def return_city(poi):
    global poi_location_data
    for city in poi_location_data.keys():
        for district in poi_location_data[city].keys():
            for point in poi_location_data[city][district]:
                if(point['Name']==poi):
                    return city
    return ''

for key in article_poi_data.keys():
    for poi in article_poi_data[key]:
        city = return_city(poi)
        if(city!=''):
            if(city not in result.keys()):
                result[city] = 1
            else:
                result[city] += 1
with open('poi_city.json','w') as file:
    json.dump(result,file,ensure_ascii=False)