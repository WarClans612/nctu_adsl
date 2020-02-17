import json

data_file = open('poi_data/article2POIlist.json',encoding='utf-8-sig')
data = json.loads(data_file.read())

seq2urls = {}
for key in data.keys():
    seq_str = str(data[key])
    if(seq_str in seq2urls.keys()):
        seq2urls[seq_str].append(key)
    else:
        seq2urls[seq_str] = [key]

with open('poi_data/POIseq2articles.json', 'w') as outfile:
        json.dump(seq2urls, outfile,ensure_ascii=False)
