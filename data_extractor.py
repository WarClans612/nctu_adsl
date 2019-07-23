#!/usr/bin/env python
# coding: utf-8
# Developer: Wilbert (wilbert.phen@gmail.com)

import gzip
import re

FOLDER = {
    'pixnet_dataset/Google Search 關鍵字log/': ['PIXNET_search_log_000000000000.gz', 'PIXNET_search_log_000000000001.gz',
        'PIXNET_search_log_000000000002.gz', 'PIXNET_search_log_000000000003.gz', 'PIXNET_search_log_url_articles.gz'],
    'pixnet_dataset/HotelsCombined API/':  ['Hackathon_Hotels_TW_CN.csv', 'Hackathon_Hotels_TW_EN.csv', 
        'HotelsCombined API -Hackathon.pdf', 'Themes.xlsx']

}

def googleData(data = None):
    '''
        data is string for the filename
        If data is none, then it will iterate through all the file
    '''
    root = 'pixnet_dataset/Google Search 關鍵字log/'
    if data is None:
        googleDataset = FOLDER[root]
    else:
        googleDataset = [data]
    for data in googleDataset:
        with gzip.open(root + data, mode='rb') as f:
            for line in f:
                line = line.decode('utf8')
                line = re.search('{.*}', line).group(0)
                yield line



if __name__ == '__main__':
    dataset = googleData()
    for index, data in enumerate(dataset):
        print(data)
        if index == 10:
            break
