#!/usr/bin/env python
# coding: utf-8
# Developer: Wilbert (wilbert.phen@gmail.com)

import gzip
import zipfile
import os
import re
import pandas as pd

pixnetFolder = {
    'pixnet_dataset/Google Search 關鍵字log/': ['PIXNET_search_log_000000000000.gz', 'PIXNET_search_log_000000000001.gz',
        'PIXNET_search_log_000000000002.gz', 'PIXNET_search_log_000000000003.gz', 'PIXNET_search_log_url_articles.gz'],
    'pixnet_dataset/HotelsCombined API/':  ['Hackathon_Hotels_TW_CN.csv', 'Hackathon_Hotels_TW_EN.csv', 
        'HotelsCombined API -Hackathon.pdf', 'Themes.xlsx'],
    'pixnet_dataset/HotelsCombined 導流 log - PIXNET 瀏覽 logs/': ['HotelsCombined_log.gz', 'HotelsCombined_log_referrer_url_articles.zip']

}

def GoogleData(data = None):
    '''
        data is string for the filename
        If data is none, then it will iterate through all the file
    '''
    root = 'pixnet_dataset/Google Search 關鍵字log/'
    if data is None:
        googleDataset = pixnetFolder[root]
    else:
        googleDataset = [data]
    for data in googleDataset:
        filename = os.path.join(os.path.dirname(__file__), root + data)
        with gzip.open(filename, mode='rb') as f:
            for line in f:
                line = line.decode('utf8')
                line = re.search('{.*}', line).group(0)
                yield line

def HotelsCombinedAPI():
    root = 'pixnet_dataset/HotelsCombined API/'
    filename = os.path.join(os.path.dirname(__file__), root + 'Hackathon_Hotels_TW_CN.csv')
    chinese_csv = pd.read_csv(filename)

    filename = os.path.join(os.path.dirname(__file__), root + 'Hackathon_Hotels_TW_EN.csv')
    english_csv = pd.read_csv(filename)

    filename = os.path.join(os.path.dirname(__file__), root + 'Themes.xlsx')
    themes = pd.read_excel(filename)

    return chinese_csv, english_csv, themes

def HotelsPixnetlog(data = None):
    '''
        data is string for the filename
        If data is none, then it will iterate through all the file
    '''
    print('something')
    root = 'pixnet_dataset/HotelsCombined 導流 log - PIXNET 瀏覽 logs/'
    if data is None:
        HotelsPixnetDataset = pixnetFolder[root]
    else:
        HotelsPixnetDataset = [data]
    for data in HotelsPixnetDataset:
        filename = os.path.join(os.path.dirname(__file__), root + data)
        if data.endswith('.gz'):
            with gzip.open(filename, mode='rb') as f:
                for line in f:
                    line = line.decode('utf8')
                    line = re.search('{.*}', line)
                    if line is not None:
                        yield line.group(0)
        elif data.endswith('.zip'):
            with zipfile.ZipFile(filename, mode='r') as z:
                for info in z.infolist():
                    print(info)
                    with z.open(info, mode='r') as f:
                        for line in f:
                            line = line.decode('utf8')
                            line = re.search('{.*}', line)
                            if line is not None:
                                yield line.group(0)


if __name__ == '__main__':
    dataset = GoogleData()
    for index, data in enumerate(dataset):
        print(data)
        if index == 10:
            break

    dataset = HotelsCombinedAPI()
    print(dataset[0])
    print(dataset[1])
    print(dataset[2])

    dataset = HotelsPixnetlog('HotelsCombined_log_referrer_url_articles.zip')
    for index, data in enumerate(dataset):
        print(data)
        if index == 10:
            break