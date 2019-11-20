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
    
# Calculate the score of cleaness
def Score_Cleaness(data,positive_var_list,integer_var_list,bool_var_list=None):
    
    # Calculate the score based on the number of na cells
    total_num=data.shape[0]*data.shape[1]
    na_num = sum(data.isnull().sum())
    na_percen = na_num/total_num
    
    # Check missing values for each column
    na_num_df=pd.DataFrame({'total':[na_num]})
    for i in list(data.columns.values):
        temp_num=data[i].isnull().sum()
        temp_df=pd.DataFrame({i:[temp_num]})
        na_num_df=pd.concat([na_num_df,temp_df],axis=1)    


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
            
    inco_percen = incor_num/total_num
    
    #Calcuate final score
    score_final=100-100*(na_percen+inco_percen)
    
    print("\nThe total number of NA value in our original data set is: ",na_num, ", and the percentage of it is: ",na_percen)
    print("\nThe total number of incorrect value in our original data set is: ",incor_num, ", and the percentage of it is: ",inco_percen)

    
    return(na_num_df,incor_num,score_final)

# Transform Categorical variables into dummies:     
def Category_to_Dummy(data,category_var_list):
    for i in category_var_list:
        # Create dummies variables and concatenate them
        dummies=pd.get_dummies(data[i])
        data=pd.concat([data,dummies],axis=1)
        
        # Drop the categorical variable
        data=data.drop([i],axis=1)
        
    return (data)

    
# Glance at the data   
def Glancing_Data(data):
    pd.set_option('display.max_columns', None)
    print(data['room_type'].unique())
    print(data.info())
    print(data.describe())
    

# Clean the data
def Data_Cleaning(data,positive_var_list,integer_var_list):
    data=data.dropna() 
    
    # Drop variables is not positive
    for i in positive_var_list:
        data=data.loc[~(data[i]<0)] 
     
    # Drop variables is not integer
    for i in integer_var_list:
        data=data.loc[~(data[i].apply(lambda x: math.floor(x)!= x))]
    
    return(data)
    
# Change upper case into lower case  
def LowerCase(data,var):
    for i in var:
        data[i]=data[i].str.lower()
    return (data)

def Airbnb_Cleanliness():
    
    filename="Airbnb_listings.csv"
    airbnb_df=Get_Airbnb_Data(filename)
    
    # Define lists to store columns' names based on their types
    positive_var_list = {'price','bathrooms','bedrooms','beds','guests_included','zipcode','accommodates','latitude'}
    integer_var_list = {'bedrooms','beds','guests_included','zipcode','accommodates'}
    category_var_list = {'property_type','room_type','bed_type'}
    bool_var_list = {'host_profile_pic','identity_verified'}
    
    na_num_df,incor_num,score_final=Score_Cleaness(airbnb_df,positive_var_list,integer_var_list,bool_var_list)
    na_num_df=na_num_df.T.reset_index()
    with open('Missing&Incorrect_Airbnb.txt','w') as f:
        f.write('The missing values for each variable is: \n')
        na_num_df.to_csv(f, header=True, index=False, sep='\t', mode='a')
        f.write('\nThe total number of incorrect values is: {}.\nThe final score is: {:4.3f}.'
                .format(incor_num,score_final))
        
def HotelPrice_Cleanliness():
    filename="Hotel_prices.csv"
    data=pd.read_csv(filename,sep=',')
    hotel_df=pd.DataFrame({'price':data['price'],'hotelName':data['hotelName'],'zipcode':data['postalCode']})


    # Define lists to store columns' names based on their types
    positive_var_list = {'price'}
    integer_var_list = {}
    
    na_num_df,incor_num,score_final=Score_Cleaness(hotel_df,positive_var_list,integer_var_list)
    na_num_df=na_num_df.T.reset_index()
    with open('Missing&Incorrect_HotelPrice.txt','w') as f:
        f.write('The missing values for each variable is: \n')
        na_num_df.to_csv(f, header=True, index=False, sep='\t', mode='a')
        f.write('\nThe total number of incorrect values is: {}.\nThe final score is: {:4.3f}.'
                .format(incor_num,score_final))

def YelpData_Cleanliness():
    filename="YelpData.csv"
    data=pd.read_csv(filename,sep=',')
    hotel_df=pd.DataFrame({'zipcode':data['zipcode'],'rating':data['rating'],'review_count':data['review_count']})


    # Define lists to store columns' names based on their types
    positive_var_list = {'rating','review_count'}
    integer_var_list = {'review_count','zipcode'}
    
    na_num_df,incor_num,score_final=Score_Cleaness(hotel_df,positive_var_list,integer_var_list)
    na_num_df=na_num_df.T.reset_index()
    with open('Missing&Incorrect_YelpData.txt','w') as f:
        f.write('The missing values for each variable is: \n')
        na_num_df.to_csv(f, header=True, index=False, sep='\t', mode='a')
        f.write('\nThe total number of incorrect values is: {}.\nThe final score is: {:4.3f}.'
                .format(incor_num,score_final))
    


if __name__ == "__main__":
    Airbnb_Cleanliness()
    HotelPrice_Cleanliness()
    YelpData_Cleanliness()
        
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
     host_profile_pic
     identity_verified
     zipcode
     latitude
     longitude

"""   
     
     
     