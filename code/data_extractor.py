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
    'pixnet_dataset/HotelsCombined 導流 log - PIXNET 瀏覽 logs/': ['HotelsCombined_log.gz', 'HotelsCombined_log_referrer_url_articles.zip'],
    'pixnet_dataset/HotelsCombined 導流 log - 交易紀錄數量資料/': ['HotelsCombined_transaction_record.gz', 'HotelsCombined_Zone_欄位說明.pdf'],
    'pixnet_dataset/使用者瀏覽log/': ['PIXNET_visit_log_000000000000.gz', 'PIXNET_visit_log_000000000001.gz',
        'PIXNET_visit_log_000000000002.gz', 'PIXNET_visit_log_000000000003.gz', 'PIXNET_visit_log_000000000004.gz',
        'PIXNET_visit_log_000000000005.gz', 'PIXNET_visit_log_url_articles.gz'],
    'pixnet_dataset/使用者點擊log/': ['PIXNET_event_log_000000000000.gz', 'PIXNET_event_log_000000000001.gz',
        'PIXNET_event_log_000000000002.gz', 'PIXNET_event_log_000000000003.gz', 'PIXNET_event_log_000000000004.gz',
        'PIXNET_event_log_000000000005.gz', 'PIXNET_event_log_000000000006.gz', 'PIXNET_event_log_url_articles.zip'],
    'pixnet_dataset/文章資料集/': ['articles_182k.gz']
}

def gzipReadLines(filename):
    with gzip.open(filename, mode='r') as f:
        for line in f:
            line = line.decode('utf8', errors="ignore")
            yield line

def zipReadLines(filename):
    with zipfile.ZipFile(filename, mode='r') as z:
        for info in z.infolist():
            with z.open(info, mode='r') as f:
                for line in f:
                    line = line.decode('utf8', errors="ignore")
                    yield line, info

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
        for line in gzipReadLines(filename):
            line = re.search('{.*}', line)
            if line is not None:
                yield line.group(0)

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
    root = 'pixnet_dataset/HotelsCombined 導流 log - PIXNET 瀏覽 logs/'
    if data is None:
        HotelsPixnetDataset = pixnetFolder[root]
    else:
        HotelsPixnetDataset = [data]
    for data in HotelsPixnetDataset:
        filename = os.path.join(os.path.dirname(__file__), root + data)
        if data.endswith('.gz'):
            for line in gzipReadLines(filename):
                line = re.search('{.*}', line)
                if line is not None:
                    yield line.group(0)
        elif data.endswith('.zip'):
            for line, _ in zipReadLines(filename):
                line = re.search('{.*}', line)
                if line is not None:
                    yield line.group(0)

def HotelsPixnetTransaction():
    root = 'pixnet_dataset/HotelsCombined 導流 log - 交易紀錄數量資料/'
    filename = os.path.join(os.path.dirname(__file__), root + 'HotelsCombined_transaction_record.gz')
    for line in gzipReadLines(filename):
        line = re.search('{.*}', line)
        if line is not None:
            yield line.group(0)

def VisitLog(data = None):
    '''
        data is string for the filename
        If data is none, then it will iterate through all the file
    '''
    root = 'pixnet_dataset/使用者瀏覽log/'
    if data is None:
        userVisitDataset = pixnetFolder[root]
    else:
        userVisitDataset = [data]
    for data in userVisitDataset:
        filename = os.path.join(os.path.dirname(__file__), root + data)
        for line in gzipReadLines(filename):
            line = re.search('{.*}', line)
            if line is not None:
                yield line.group(0)

def EventLog(data = None):
    '''
        data is string for the filename
        If data is none, then it will iterate through all the file
    '''
    root = 'pixnet_dataset/使用者點擊log/'
    if data is None:
        userEventDataset = pixnetFolder[root]
    else:
        userEventDataset = [data]
    for data in userEventDataset:
        filename = os.path.join(os.path.dirname(__file__), root + data)
        if data.endswith('.gz'):
            for line in gzipReadLines(filename):
                line = re.search('{.*}', line)
                if line is not None:
                    yield line.group(0)
        elif data.endswith('.zip'):
            for line, _ in zipReadLines(filename):
                line = re.search('{.*}', line)
                if line is not None:
                    yield line.group(0)

def PixnetArticle():
    root = 'pixnet_dataset/文章資料集/'
    filename = os.path.join(os.path.dirname(__file__), root + 'articles_182k.gz')
    for line in gzipReadLines(filename):
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
        if index == 1:
            break

    dataset = HotelsPixnetTransaction()
    for index, data in enumerate(dataset):
        print(data)
        if index == 10:
            break

    dataset = VisitLog('PIXNET_visit_log_url_articles.gz')
    for index, data in enumerate(dataset):
        print(data)
        if index == 10:
            break

    dataset = EventLog('PIXNET_event_log_url_articles.zip')
    for index, data in enumerate(dataset):
        print(data)
        if index == 10:
            break

    dataset = PixnetArticle()
    for index, data in enumerate(dataset):
        print(data)
        if index == 10:
            break
