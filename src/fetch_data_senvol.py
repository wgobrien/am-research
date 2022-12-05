#!/usr/bin/python3
# fetch_data_senvol.py
# William O'Brien 11/23/2022

import requests
from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup as bs

import pandas as pd

import re
import os

def fetch():
    print("--------------------\nFetching Data\n--------------------")
    argc = len(sys.argv)
    # optional usuage: fetch_data_senvol.py <file_path> <file_name>
    
    if argc == 1:
        # optional: can edit file out name on command line
        out_name = 'interim_data'
    elif argc == 2:
        out_name = sys.argv[1]
    else:
        print('usuage: fetch_data_senvol.py <data_out_name>')
        exit(1)

    session = AsyncHTMLSession()
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'}

    page_rows = []
    page_num = 1
    res = 0
    total = 1
    headers_found = False

    while res != total:
        
        # get url, increment page number for next scrape
        url = f'http://senvol.com/5_material-results/?appSession=0LTD9N6NY50DFEC28SO9N86TP49WFI6R6GEO4242743X1UP61EW017ASO6LS75SQX9CX2NW0G6Z6G8S456523E2RT203784AYQ578JEI6N0Q1I1MF957ZES52XGY3K38&PageID=2&PrevPageID=&cpipage={page_num}&CPISortType=&CPIorderBy=&appSession=26D32R65NSJT4F758HXOR2LE407P1479FX808Z5288IX77J2J5XK0RJX1Q99KFV05V5FF5K5Z1PHFF754130M6P3SQZ7CU1KUE5J5O367I9OG0YOL8WD1HH6D2D3F802&PageID=2&PrevPageID=&cpipage=2&CPISortType=&CPIorderBy='
        page_num += 1
        
        # pull html data, run through beautiful soup
        r = session.get(url,headers=headers)
        r.html.arender(timeout=20, retries=3)
        resp = r.html.raw_html
        soup = bs(resp, 'html.parser')
        
        # extract table, add rows to page_rows
        table = soup.find('table', {'id':re.compile(r'cbTable_')})
        rows = table.find_all('tr', {'id':re.compile(r'DataRow')})
        for row in rows:
            page_rows.append([item.text for item in row.find_all('td')])
        
        # get header info
        if not headers_found:
            header_raw = table.find('tr', class_=re.compile(r'cbResultSetTableHeader_'))
            header = [label.text for label in header_raw.find_all('th', class_=re.compile(r'cbResultSetHeaderCell'))]
            headers_found = True
        
        # check if we should stop searching pages
        record_text = soup.find('td', class_=re.compile(r'cbResultSetRecordMessage_')).text
        nums = re.findall(r'\d+', record_text)
        res = nums[1]
        total = nums[2]
        
        print(f'page {page_num-1}: results {res} of {total} scraped')
    
    senvol_df = pd.DataFrame(page_rows, columns=header)

    print("\nexporting data to csv...")
    
    out_path = os.path(f'../data/interim/{out_name}.csv')
    f_out = os.path.join(os.path.dirname(__file__), out_path)
    senvol_df.to_csv(f_out)

    print("\ndone.")

if __name__ == '__main__':
    fetch()
