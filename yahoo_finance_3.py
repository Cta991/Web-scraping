import urllib.request
import ssl
from bs4 import BeautifulSoup as bs
import sqlite3

#Ignore certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Retrieve data
url = input("Enter url: ")
data = urllib.request.urlopen(url, context=ctx).read()
html = bs(data, "html.parser")

#Store data
lst, lst_info, info = [], [], []
tags_div = html('div')
for tag in tags_div:
    attr = tag.attrs
    if ('data-test', 'quote-header') in attr.items():
        for item in tag.find_all('h1'):
            Name = item.text
    if ('data-reactid', '31') in attr.items() and "Current price" not in lst_info:
        lst_info.append("Current price")
        info.append(tag.text)
    if ('data-test', 'left-summary-table') in attr.items():
        for item in tag.find_all('td'):
            lst.append(item.text)
    if ('data-test', 'right-summary-table') in attr.items():
        for item in tag.find_all('td'):
            lst.append(item.text)

#Seperate data into 2 lists
for i in range(len(lst)):
    if i%2==0: lst_info.append(lst[i])
    else: info.append(lst[i])

#Save the data into a database
conn = sqlite3.connect('yahoo_finance.sqlite')
cur = conn.cursor()

try: cur.execute('''
CREATE TABLE Financial_info(
    Name TEXT UNIQUE
);
''')
except:
    print('Updating table...')
for item in lst_info:
        try:
            line = 'ALTER TABLE Financial_info ADD COLUMN "' + item + '" TEXT'
            cur.execute(line)
        except: continue
line = 'INSERT INTO Financial_info (Name) VALUES ("' + Name + '")'
try:
    cur.execute(line)
except:
    print(Name, 'already in table, updating information...')
for i in range(len(lst_info)):
    line = 'UPDATE Financial_info SET "'+lst_info[i]+'"="'+info[i]+'" WHERE Name="'+Name+'"'
    cur.execute(line)
conn.commit()
print("Done")
