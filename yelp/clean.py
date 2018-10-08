#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 17:20:58 2018

@author: OliverQiu
"""

import pandas as pd

def main():
    
    data = pd.read_csv('dirty_results.csv')
    Combine_Zipcode(data)


def Combine_Zipcode(data):
    # set up the out put file
    fieldnames= ['zipcode','count']
    CSVFILE = 'clean_data.csv'
    with open(CSVFILE, "w"):
        df = pd.DataFrame(columns = fieldnames)
        df.to_csv(CSVFILE, header=True, index=False, mode='a')
    
    # extract all unique 
    zipcode = data['zipcode'].unique()
    
    # filter
    for i in range(0,len(zipcode)):
        subset = data[data['zipcode'] == zipcode[i]]
        highrating = subset[subset['rating']>=4.6]
        cnt = highrating['rating'].count()
    
        df=df.append({
                    'zipcode': zipcode[i],
                    'count':cnt
            }, ignore_index=True)
    
    # append to output file
    df.to_csv(CSVFILE, index=None, mode='a',header=None)

main()