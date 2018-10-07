#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 10:41:53 2018

@author: stevechen
"""

import pandas as pd
import numpy as np
import math

# Read file to get wanted variables from the Airbnb data set
def Get_Airbnb_Data(filename):
    data=pd.read_csv(filename,sep=',')
    newdata_df=pd.DataFrame({'price':data['price'],'property_type':data['property_type'],
                          'room_type':data['room_type'],'accommodates':data['accommodates'],
                          'bathrooms':data['bathrooms'],'bedrooms':data['bedrooms'],
                          'beds':data['beds'],'bed_type':data['bed_type'],
                          'guests_included':data['guests_included'],
                          'host_profile_pic':data['host_has_profile_pic'],'identity_verified':data['host_identity_verified'],
                          'zipcode':data['zipcode'],'latitude':data['latitude'],'longitude':data['longitude']})

    return (newdata_df)
    

def Score_Cleaness(data,positive_var_list,integer_var_list,bool_var_list=None):
    
    # Calculate the score based on the number of na cells
    total_num=data.shape[0]*data.shape[1]
    na_num = sum(data.isna().sum())
    na_percen = (total_num-na_num)/total_num

       
    # Define a function to determine a number whether is an integer or not.
    # Let us omit the na and find the incorrect value
    incor_num=0
    # Find all negative value
    for i in positive_var_list:
        # Let us omit the na and find the incorrect value
        temp=data.loc[~(np.isnan(data[i]))]       
        # Find all negative number
        incor_num=incor_num+sum(temp[i].apply(lambda x: x<0))
    
    # Find all non integer value
    for i in integer_var_list:
        # Let us omit the na  and negative number,and find the incorrect value
        temp=data.loc[~(np.isnan(data[i]))]
        temp=temp.loc[~(temp[i]<0)]       
        # Find all non integer number
        incor_num=incor_num+sum(temp[i].apply(lambda x: math.floor(x) != x))
    
    
    if bool_var_list!=None:
        for i in bool_var_list:
            temp=data.loc[~(pd.isnull(data['bedrooms']))]
            incor_num=incor_num+sum(temp[i].apply(lambda x: x != 't' and x != 'f' and x!='true' and x!='false' and x!='1' and x!='0'))
            
    inco_percen = (total_num-incor_num)/total_num
    
    #Calcuate final score
    score_final=50*(na_percen+inco_percen)   
    return(score_final)

# Transform Categorical variables into dummies:     
def Category_to_Dummy(data,category_var_list):
    for i in category_var_list:
        # Create dummies variables and concatenate them
        dummies=pd.get_dummies(data[i])
        data=pd.concat([data,dummies],axis=1)
        
        # Drop the categorical variable
        data=data.drop([i],axis=1)
        
    return (data)

    
    
def Glancing_Data(data):
    pd.set_option('display.max_columns', None)
    print(data['room_type'].unique())
    print(data.info())
    print(data.describe())
    

def Data_Cleaning(data,positive_var_list,integer_var_list):
    data=data.dropna() 
    
    # Drop variables is not positive
    for i in positive_var_list:
        data=data.loc[~(data[i]<0)] 
     
    # Drop variables is not integer
    for i in integer_var_list:
        data=data.loc[~(data[i].apply(lambda x: math.floor(x)!= x))]
    
    return(data)
    
  
def LowerCase(data,var):
    for i in var:
        data[i]=data[i].str.lower()
    return (data)


def main():
    # Read Data
    filename="nyc1k.csv"
    airbnb_df=Get_Airbnb_Data(filename)
    #Glancing_Data(airbnb_df)
    
    # Define lists to store columns' names based on their types
    positive_var_list = {'price','bathrooms','bedrooms','beds','guests_included','zipcode','accommodates','latitude'}
    integer_var_list = {'bedrooms','beds','guests_included','zipcode','accommodates'}
    category_var_list = {'property_type','room_type','bed_type'}
    bool_var_list = {'host_profile_pic','identity_verified'}
    
    
    # Change upper case to lower case
    airbnb_df=LowerCase(airbnb_df,bool_var_list)
    
    # Calculate score before cleaning
    score_b4_cleaned=Score_Cleaness(airbnb_df,positive_var_list,integer_var_list,bool_var_list=bool_var_list)    
    print("Score before cleaned is:",score_b4_cleaned)
    
    # Clean the data
    airbnb_df=Data_Cleaning(airbnb_df,positive_var_list,integer_var_list)
    
    
    score_after_cleaned=Score_Cleaness(airbnb_df,positive_var_list,integer_var_list,bool_var_list=bool_var_list)
    print("Score after cleaned is:",score_after_cleaned)
    airbnb_df=Category_to_Dummy(airbnb_df,category_var_list)
    


        
        

if __name__ == "__main__":
    main()

        
"""    
We will use below variables for airbnb
     price
     property_type
     room_type
     accommodates
     bathrooms
     bedrooms
     beds
     bed_type
     square_feet     
     guests_included
     host_neighbourhood
     host_has_profile_pic
     host_identity_verified
     zipcode
     latitude
     longitude
     host_total_listings_count
"""   
     
     
     