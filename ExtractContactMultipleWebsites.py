# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 15:37:34 2018
Topic : Firstly, Search google upto 10 pages and scrap all the URL titles, urls and description. Secondly, Scrap each of the URL and 
extract contact details eg: Phone number, email address and city/Country. Store ALl the information in json format.
All the exceptions and errors are handled properly.
@author: Nagesh Singh Chauhan
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib2 import urlopen,urlparse, Request,HTTPError
import urllib2
import re
import numpy as np
import csv
from httplib import BadStatusLine
import ssl
import json

class Google:
    @classmethod
    def search1(self, search):
      url_list = []   #store all the extracted urls in a List
      title_list = [] #store all the extracted titles in a List
      description_list = []  #store all the extracted Description in a List

      for start in range(0,10):
          page = requests.get('http://www.google.de/search?q='+search+str(start*10), verify = False)
          soup = BeautifulSoup(page.text,'html.parser')

          for cite in soup.findAll('a', attrs={'class':'r'}): #extrcat all URLs
              url = cite.text
              print url
              if not urlparse.urlparse(url).scheme: #check if url has prefix http:// or not
	             url = 'http://'+url
	             print url
              url_list.append(url.replace('https://','http://')) 
          for tit in soup.findAll('div', attrs={'class':'ellip'}): #extract all Titles
              print tit.text
              title_list.append(tit.text)
            
       
          for descr in soup.findAll('span', attrs={'class':'st'}): #extraxt all description
              print descr.text
              description_list.append(descr.text)

      print title_list
"""
      record_list = [list(item) for item in list(zip(url_list, title_list, description_list))] #join all the lists
      df = pd.DataFrame(record_list,columns=['URL','Title', 'Description'])
      print df
      df.to_csv('result_url_topic_desc.csv', index=False, encoding='utf-8') 
      with open('result_url_topic_desc.csv') as f:
           reader = csv.DictReader(f)
           rows = list(reader)
      with open('result_url_topic_desc_JSON.json', 'w') as f:
           json.dump(rows, f, sort_keys=False, indent=4, separators=(',', ': '),encoding='utf-8') 
    
"""
user_input = raw_input("Enter your search string : ")
Google.search1(user_input) # user search string
#Google.search1('cloud managed services') # user search string

df2=pd.DataFrame()
df2 = pd.read_csv('result_url_topic_desc.csv', encoding='utf-8')
phn_1 = []    #store all the extracted Phn numbers in a List
mail_1 = []    #store all the extracted E-mail in a List
for row in df2.iterrows():  # Parse through each url in the list.
    try:
        try:
           req1 = Request(row[1]['URL'], headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'})
           gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23) # Bypass SSL certification verification
           f = urlopen(req1, context=gcontext)
           url_name = f.geturl() #extract URL name 
           s = f.read()
           phone = re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})",s)  # Phone regex
           emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}",s)  #Email regex

           if len(phone) == 0:
              print("No phone number found.")
              err_msg_phn = "No phone number found."
              phn_1.append((url_name, err_msg_phn))
              
           else:
               count = 1
               for item in phone:
                   phn_1.append((url_name,item))
                   count += 1
               print(phn_1)
        
           if len(emails) == 0:
              print("No email address found.")
              err_msg_mail = "No email address found."
              mail_1.append((url_name,err_msg_mail))

           else:
               count = 1
               for item in emails:
                   mail_1.append((url_name,item))
                   count += 1
               print(mail_1)
               
        except BadStatusLine: # Catch if invalid url names exist
            print("could not fetch %s" % url_name)

    except urllib2.HTTPError as err: # catch HTTP 404 not found error
        if err == 404:
            print("Received HTTPError on %s" % url_name)
            

df_p = pd.DataFrame()
df_m = pd.DataFrame()
df_final = pd.DataFrame()

df_p = pd.DataFrame(phn_1,columns=['URL','Phone_No']) # Dataframe for url and Phn number
df_phn = df_p.drop_duplicates(subset=['URL', 'Phone_No'], keep='first') #remove duplicates

df_m = pd.DataFrame(mail_1,columns=['URL','Email']) # Dataframe for url and Email
df_mail = df_m.drop_duplicates(subset=['URL','Email'], keep='first') #remove duplicates

df_final = pd.merge(df_phn,df_mail, on = 'URL', how = 'inner') #Merge two dataframes on the common column
#df_final.groupby(['URL'], as_index=False)
df_final.to_csv('result_contact.csv', index=False, encoding='utf-8')

#convert the csv output to json
with open('result_contact.csv') as f:
     reader = csv.DictReader(f)
     rows = list(reader)
#with open('result_contact_JSON.json', 'w') as f: 
#   json.dump(rows, f, sort_keys=False, indent=4, separators=(',', ': '),encoding='utf-8')
