#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 19:44:57 2023

@author: ulanamanakova
"""

from bs4 import BeautifulSoup
import json
import requests
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_largest_banks"
html_data  = requests.get(url).text

soup = BeautifulSoup(html_data, "html.parser")
#print(soup)

tables = soup.find_all('table')
table_index = -1
for index,table in enumerate(tables): #h2 = "By market capitalization"
    if ("Bank name" in str(table)): #table name in h2, not in the table
        table_index = index
#        print("index")
#print(table_index)

data = pd.DataFrame(columns=["Name", "Market Cap (US$ Billion)"])

#for row in soup.find_all('tbody')[3].find_all('tr'):
col1 = []
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all('td') #a href - bank name
    if (col != []):
        na = col[1].find_all('title')
        name = col[1].text
        cap = col[2].text
        dt1 = pd.DataFrame.from_records([{"Name":name.strip('\n'), "Market Cap (US$ Billion)":cap.strip('\n')}])
        data = pd.concat([data, dt1], ignore_index=True)

#print(data)

dj = data.to_json()
with open('bank_market_cap.json', 'w') as f:  # writing JSON object
    json.dump(dj, f)




