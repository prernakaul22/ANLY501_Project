from lxml import html  
import csv
import requests
from time import sleep
import re
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse(url,zipcode,df):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    response = requests.get(url, headers=headers, verify=False).text
    parser = html.fromstring(response)
    print ("Parsing the page")
    listing = parser.xpath("//li[@class='regular-search-result']")
    scraped_datas=[]
    for results in listing:
        raw_position = results.xpath(".//span[@class='indexed-biz-name']/text()")   
        raw_name = results.xpath(".//span[@class='indexed-biz-name']/a//text()")
        raw_ratings = results.xpath(".//div[contains(@class,'rating-large')]//@title")
        raw_review_count = results.xpath(".//span[contains(@class,'review-count')]//text()")
        raw_price_range = results.xpath(".//span[contains(@class,'price-range')]//text()")
        category_list = results.xpath(".//span[contains(@class,'category-str-list')]//a//text()")
        raw_address = results.xpath(".//address//text()")
        is_reservation_available = results.xpath(".//span[contains(@class,'reservation')]")
        is_accept_pickup = results.xpath(".//span[contains(@class,'order')]")
        

        name = ''.join(raw_name).strip()
        position = ''.join(raw_position).replace('.','')
        cleaned_reviews = ''.join(raw_review_count).strip()
        reviews =  re.sub("\D+","",cleaned_reviews)
        categories = ','.join(category_list) 
        cleaned_ratings = ''.join(raw_ratings).strip()
        if raw_ratings:
            ratings = re.findall("\d+[.,]?\d+",cleaned_ratings)[0]
        else:
            ratings = 0
        price_range = len(''.join(raw_price_range)) if raw_price_range else 0
        address  = ' '.join(' '.join(raw_address).split())
        reservation_available = True if is_reservation_available else False
        accept_pickup = True if is_accept_pickup else False
        df=df.append({
                'zipcode': zipcode,
                'business_name':name,
                'rank':position,
                'review_count':reviews,
                'categories':categories,
                'rating':ratings,
                'address':address,
                'reservation_available':reservation_available,
                'accept_pickup':accept_pickup,
                'price_range':price_range
        }, ignore_index=True)
        
    return df

if __name__=="__main__":
    # input all NYC zipcode
    INFILE = 'Zipcode.txt'
    
    ## input data from txt file
    with open(INFILE,'rt') as file:
        zipcode = []
        for lines in file:
            #get rid of the \n in each line
            lines=lines.strip('\n')
            zipcode.append(lines)
    
    # set up output file
    CSVFILE = 'yelp_results.csv'
    fieldnames= ['zipcode','business_name','rank','review_count','categories','rating','address','reservation_available','accept_pickup','price_range','url']
    
    with open(CSVFILE, "w"):
        df = pd.DataFrame(columns = fieldnames)
        df.to_csv(CSVFILE, header=True, index=False, mode='a') 
        
        
    # set parameter
    search_query = 'Restaurants'

    for i in range(0,len(zipcode)):
        # set parameter
        place = zipcode[i]

        for count in range(0,10):
            # set parameter
            rank_num = 30*count

            yelp_url  = "https://www.yelp.com/search?find_desc=%s&find_loc=%s&start=%s"%(search_query,place,rank_num)
            
            print ("Retrieving :",place)
            x = pd.DataFrame(columns = fieldnames)
            x = parse(yelp_url,place,x)

            print ("Writing data to output file")
            x.to_csv("yelp_results.csv", index=None, mode='a',header=None)
            
            sleep(2)

      
               


