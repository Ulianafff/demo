#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:45:36 2023
"""

import pandas as pd
from datetime import date

df = pd.read_csv("/Users/ulanamanakova/Documents/PyPs/DATASETS/waste_star/DataForCognos.csv")

d = date(int("20"+df["Date"][2][6:8]), int(df["Date"][2][3:5]), int(df["Date"][2][0:2]))

dddf = pd.DataFrame()

for dat in df["Date"]:
    d = date(int("20"+dat[6:8]), int(dat[3:5]), int(dat[0:2]))
    dddf = dddf.append(pd.Series(d), ignore_index=True)

df["Date"] = dddf
#print(df.tail(10))

df.to_csv('DataForCognos2.csv', index = False)
