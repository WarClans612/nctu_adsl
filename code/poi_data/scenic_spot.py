import json
import pandas as pd
import re

#create an alias name based on cleaning name with keyword list
def return_clean_name(name):
    global keyword_list
    ori_name = name
    for keyword in keyword_list:
        ori_name = ori_name.replace(keyword,'')
    return ori_name

#create a list of alias name based on punctuation
def return_punctuation_name(name):
    global punctuation_list
    punc_name_list = []
    rm_punc_name = return_clean_name(name)
    for punc in punctuation_list:
        rm_punc_name = rm_punc_name.replace(punc,'')
    if(rm_punc_name != rm_punc_name):
        punc_name_list.append(rm_punc_name)
    
    for punc in punctuation_list:
        punc_seperate_name = []
        punc_seperate_name = name.split(punc)
        if(len(punc_seperate_name)>1):
            punc_name_list += punc_seperate_name

    return punc_name_list

def return_brackets_name(name):
    brackets_list = []
    tmp = name
    tmp = tmp[tmp.find("(")+1:tmp.find(")")]
    #print(tmp)
    if(len(tmp)>1 and tmp!=name[:-1]):
        #brackets_list.append(tmp)
        brackets_list.append(name.replace('('+tmp+')',''))
    return brackets_list

#create alias list based on entity name
def return_alias_list(name):
    alias_list = []
    alias_list.append(name)

    ori_name = return_clean_name(name)
    if(name!=ori_name):
        alias_list.append(ori_name)
    
    alias_list += return_punctuation_name(name)

    alias_list += return_brackets_name(name)

    for alias in alias_list:
        if(len(alias)<2):
            alias_list.remove(alias)
    return alias_list

#unsless key list for key,value pair drop
useless_key = ['Picture1','Picdescribe1','Picture2','Picdescribe2','Picture3','Picdescribe3','Class1','Class2','Class3','Level','Map']

#punctuation
punctuation_list = ['˙','，','-','：',':','、']

#keyword file for creating alias names
keyword_file = open('keyword.txt','r')
keyword_list = eval(keyword_file.read())

#read scenic spot data
data_file = open('scenic_spot_C_f_with_pic.json',encoding='utf-8-sig')
data = json.loads(data_file.read())
data_list = data['XML_Head']['Infos']['Info']

#drop useless key,value pair
#for poi in data_list:
#    for key in useless_key:
#        del poi[key]

for i in range(len(data_list)):
    data_list[i]['alias'] = return_alias_list(data_list[i]['Name'])
    #print(data_list[i]['Name'],data_list[i]['alias'])

data['XML_Head']['Infos']['Info'] = data_list

with open('scenic_spot_with_alias.json', 'w') as outfile:
    json.dump(data, outfile,ensure_ascii=False)
