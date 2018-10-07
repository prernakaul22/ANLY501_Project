#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 15:13:37 2018

@author: katezeng
"""

# Libraries
import pandas as pd

# functions
def drop_zipcodes(df1, df2):
    zipcode1 = list(df1['zipcode'])
    zipcode2 = list(df2['zipcode'])
    for zips in zipcode1:
        if zips not in zipcode2:
            df1 = df1[df1.zipcode != zips]
    return df1

def main():
    # read in data
    raw_data = pd.read_csv('./data/nyc.csv', low_memory = False)
    
    # drop irrelavant columns
    drop_list = ['listing_url', 'scrape_id', 'last_scraped', 'name', 'summary', 'space', 'description', 
                 'experiences_offered', 'neighborhood_overview', 'notes', 'transit', 'access', 'interaction',
                 'house_rules', 'thumbnail_url', 'medium_url', 'picture_url', 'xl_picture_url', 'host_url', 
                 'host_name', 'host_location', 'host_about', 'host_acceptance_rate', 'host_thumbnail_url', 
                 'host_picture_url', 'neighbourhood', 'calendar_updated', 'calendar_last_scraped', 'license', 
                 'jurisdiction_names', 'host_id']
    data = raw_data.drop(columns = drop_list)
    
    # drop listings outside US
    data = data[data.country_code == 'US']
    data['zipcode'] = data['zipcode'].astype(str)
    
    # save rows with zipcodes in NYC
    nyc_zip = pd.read_csv('./data/zipcodes.csv')
    nyc_zip['zipcode'] = nyc_zip['zipcode'].astype(str)
    
    datav1 = drop_zipcodes(data, nyc_zip)
    datav1.to_csv('./data/nycdata_v1.csv', index = False)
    
if __name__ == "__main__":
    main()