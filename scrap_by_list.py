import urllib.request
import ssl
from bs4 import BeautifulSoup as bs
import sqlite3

#Ignore certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def url_auto(tag):
    try:
        lst = []
        url = "http://books.toscrape.com/catalogue/" + tag
        data = urllib.request.urlopen(url, context=ctx).read()
        soup = bs(data, "html.parser")

        tags = soup('a')
        for tag in tags:
            lst.append(tag.get('href', None))
        tag = lst[-1]
        return tag
    except:
        print("Error")

#Create the database and add the data
conn = sqlite3.connect('book_scraping_list.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Lists')
cur.execute('CREATE TABLE Lists (name TEXT, price INTEGER)')

#Retrieve the data

end_tag, lst, lst_url = "page-1.html", [], []
url = "http://books.toscrape.com/catalogue/" + end_tag
#for u in range(1,51):
#    url = str("http://books.toscrape.com/catalogue/page-"+str(u)+".html")
while True:
    print("Connecting to url:", url)
    try:
        data = urllib.request.urlopen(url, context=ctx).read()
    except:
        break
    soup = bs(data, "html.parser")

    tags_a, lst_1 = soup('a'), []
    for tag in tags_a:
        title = tag.get('title')
        if title != None: lst_1.append(title)
    tags_p, lst_2 = soup('p'), []
    for tag in tags_p:
        try:
            price = tag.contents[0].split()[0]
            lst_2.append(price)
        except:
            continue
    print("Updating database")
    for i in range(len(lst_1)):
        cur.execute('INSERT INTO Lists (name, price) VALUES (?, ?)', (lst_1[i], lst_2[i]))
        conn.commit()
    end_tag = url_auto(end_tag)
    url = "http://books.toscrape.com/catalogue/" + end_tag
    if url in lst_url: break
    lst_url.append(url)
print('Done')
