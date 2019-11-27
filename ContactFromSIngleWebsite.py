# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 09:17:20 2018

@author: Kishore1
"""

from bs4 import BeautifulSoup
import re
import urllib2
import pandas as pd

f = urllib2.urlopen('https://www.fundoodata.com/companies-detail/Larsen-&-Toubro-Infotech-Ltd-(LTI)/32572.html')
#f = urllib.urlopen(row['URLs'])
s = f.read().decode('utf-8')

phone = re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})",s)
emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}",s)
phn_1 = []
mail_1 = []
if len(phone) == 0:
   print ("No phone number found.")
   print ()
else:
   count = 1
   for item in phone:
       phn_1.append(item)
       count += 1
   print(phn_1)   

if len(emails) == 0:
   print("No email address found.")
   print()
else:
    count = 1
    for item in emails:
        mail_1.append(item)
        count += 1
    print(mail_1)    

record_list = [list(item) for item in list(zip(mail_1,phn_1))]
df = pd.DataFrame(record_list,columns=['E-Mail','PhnNo.'])
df.to_csv('Cloud_Solutions_Provider_India.csv', index=False, encoding='utf-8')

# convert csv file into json
import csv
import json
with open('Cloud_Solutions_Provider_India.csv') as f:
     reader = csv.DictReader(f)
     rows = list(reader)
with open('Cloud_Solutions_Provider_India_JSON.json', 'w') as f:
     json.dump(record_list,f, sort_keys=False, indent=4, separators=(',', ': '),encoding='utf-8',ensure_ascii=False)

