import json

#Source data path configuration
districts_data_path = '/home/pixnet/code/poi_data/taiwan_districts_mapping.json'
poi_addr_data_path = '/home/pixnet/code/poi_data/location_POIs.json'
poiseq_data_path = '/home/pixnet/code/poi_data/POIseq2articles.json'
popularity_data_path = '/home/pixnet/code/popularity/url_popularity.json'
poi_data_path = '/home/pixnet/code/poi_data/scenic_spot_C_f_with_pic.json'
url_title_data_path = '/home/pixnet/code/WebAPI/url_title.json'

def read_data(data_path):
    data_file = open(data_path,encoding='utf-8-sig')
    data = json.loads(data_file.read())
    return data

class API:
    def __init__(self):
        global districts_data_path,poi_addr_data_path,poiseq_data_path,popularity_data_path,poi_data_path,url_title_data_path
        self.poi_data = read_data(poi_data_path)
        self.distircts_data = read_data(districts_data_path)
        self.poi_addr_data = read_data(poi_addr_data_path)
        self.poiseq_data =  read_data(poiseq_data_path)
        self.popularity_data = read_data(popularity_data_path)
        self.url_title_data = read_data(url_title_data_path)
        self.poi_info_dict = {}
        self.generate_poi_addr_dict()

    def generate_poi_addr_dict(self):
        poi_data = self.poi_data
        poi_data_list = poi_data['XML_Head']['Infos']['Info']
        for poi in poi_data_list:
            self.poi_info_dict[poi['Name']] = {}
            self.poi_info_dict[poi['Name']]['Add'] = poi['Add']
            if(poi['Picture1']!=''):
                self.poi_info_dict[poi['Name']]['pic'] = poi['Picture1']
                self.poi_info_dict[poi['Name']]['pic_des'] = poi['Picdescribe1']
            else:
                self.poi_info_dict[poi['Name']]['pic'] = 'No picture'
                self.poi_info_dict[poi['Name']]['pic_des'] = 'No picture'
    
    def parse_location(self,location):
        districts = self.distircts_data
        match_addr_list = []
        location = location.replace('台','臺')
        for key in districts.keys():
            if(key.find(location)!=-1):
                for sub_key in districts[key].keys():
                    match_addr_list.append((key,sub_key))
            else:
                for sub_key in districts[key].keys():
                    if(sub_key.find(location)!=-1):
                        match_addr_list.append((key,sub_key))
        return match_addr_list

    def all_location(self):
        districts = self.distircts_data
        addr_list = []
        for key in districts.keys():
            for sub_key in districts[key].keys():
                addr_list.append((key,sub_key))
        return addr_list
        
    def districts_to_POIs(self,addr_list):
        pois = self.poi_addr_data
        match_poi_list = []
        for key1,key2 in addr_list:
            match_poi_list += [poi['Name'] for poi in pois[key1][key2]]
        return match_poi_list

    def get_poiseq(self,pois_list):
        seqs = self.poiseq_data
        popularity = self.popularity_data
        seq_list = []
        for seq_str in seqs.keys():
            tmp_dict = {}
            add_list = []
            title_list = []
            pic_list = []
            pic_des_list = []
            seq = eval(seq_str)
            for poi in seq:
                add_list.append(self.poi_info_dict[poi]['Add'])
                pic_list.append(self.poi_info_dict[poi]['pic'])
                pic_des_list.append(self.poi_info_dict[poi]['pic_des'])
            for url in seqs[seq_str]:
                title_list.append(self.url_title_data[url])
            tmp_dict['poi_seq'] = seq
            tmp_dict['addr_seq'] = add_list
            tmp_dict['match_score'] = float(len([poi for poi in seq if(poi in pois_list)]))/float(len(seq))
            tmp_dict['popular_score'] = sum([float(popularity[url]) for url in seqs[seq_str] if popularity[url]])
            tmp_dict['url_list'] = seqs[seq_str]
            tmp_dict['title_list'] = title_list
            tmp_dict['pic_list'] = pic_list
            tmp_dict['pic_des_list'] = pic_des_list
            seq_list.append(tmp_dict)
        return seq_list

    def get_POI_addr_info(self):
        return self.poi_addr_dict
    
    def compose_poi_seqs(self,seq_list,days):
        comp_list = []
        if(days==0):
            for seq in seq_list:
                comp_list.append([seq])
        return comp_list

    def call_search_API(self,location=None,time=None,activity=None):
        if(location != None):
            addr_list = self.parse_location(location)
            pois_list = self.districts_to_POIs(addr_list)
            seq_list = self.get_poiseq(pois_list)
            seq_list = [seq for seq in seq_list if seq['match_score']>=1]
            seq_list.sort(key= lambda seq: (seq['match_score'],seq['popular_score']),reverse=True)
            #return seq_list
        else:
            addr_list = self.all_location()
            pois_list = self.districts_to_POIs(addr_list)
            seq_list = self.get_poiseq(pois_list)
            seq_list.sort(key= lambda seq: (seq['match_score'],seq['popular_score']),reverse=True)
        #TODO: process query with time and activity
        if(time == None):
            result = self.compose_poi_seqs(seq_list,0)
        else:
            result = self.compose_poi_seqs(seq_list,time)
        #if(activity=None):
        result = [poi_seq for poi_seq in result if(len(poi_seq[0]['poi_seq'])>1 and len(poi_seq[0]['poi_seq'])<5)]
        return result

"""
Usage
==============================================================
Init a API() object when starting server
Send a request with function call_API(location,time,activity)
This will return a list of dict contain POI seqeunce infos
==============================================================
"""

pixnetAPI = API()
#print(pixnetAPI.get_POI_addr_info())
output = pixnetAPI.call_search_API('台南')
output = [poi_seq for poi_seq in output if(len(poi_seq[0]['poi_seq'])>1 and len(poi_seq[0]['poi_seq'])<5)]
with open('台南_output.txt','w') as f:
    output_str = str(output)
    f.write(output_str)
print(len(output))
'''
for i in range(10):
    if(len(output[i][0]['title_list'])<1):
        print(output[i])
'''
#print([out for out in output if len(out['url_list'])>1])
#for i in range(20):
#    print(output[i])

        
