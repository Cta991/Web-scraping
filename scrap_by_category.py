import sqlite3
import ssl
import urllib.request
from bs4 import BeautifulSoup as bs
import re

conn = sqlite3.connect("book_scrap_2.sqlite")
cur = conn.cursor()
cur.executescript("""
DROP TABLE IF EXISTS Lists;
DROP TABLE IF EXISTS Category;

CREATE TABLE Lists(
    name TEXT,
    price INTEGER,
    category_id INTEGER
);
CREATE TABLE Category(
    category TEXT UNIQUE,
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE
);
""")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode - ssl.CERT_NONE
#A function that return the tags
def url_access(url, tag):
    data = urllib.request.urlopen(url, context=ctx).read()
    soup = bs(data, "html.parser")
    tags = soup(tag)
    return tags
#A function that add data to table Lists and return anchor tags
def get_info(link):
    url = link
    tags_a, lst_a = url_access(url, "a"), []
    tags_p, lst_p = url_access(url, "p"), []
    for tag in tags_a:
        title = tag.get('title')
        if title != None: lst_a.append(title)
    for tag in tags_p:
        try:
            price = tag.contents[0].split()[0]
            lst_p.append(price)
        except:
            continue
    for i in range(len(lst_a)):
        cur.execute('''INSERT INTO Lists (name,price,category_id) VALUES (?,?,?)
        ''', (lst_a[i], lst_p[i], category_id))
    return tags_a

tags_a = url_access("http://books.toscrape.com/index.html", "a")
lst_category = []
for tag in tags_a:
    link = tag.get("href", None)
    if "category" in link and "books_1" not in link: lst_category.append(link)

for tag in lst_category:
    url = "http://books.toscrape.com/" + tag
    print("Accessing:", url)
#Add data to Category
    category = re.findall("category/books/(\S*)_", url)[0]
    cur.execute("INSERT INTO Category (category) VALUES (?)", (category,))
    cur.execute("SELECT id FROM Category WHERE category = ?", (category,))
    category_id = cur.fetchone()[0]
#get the title and price from the retrieved category
    tags_a = get_info(url)
#get the next page link if exists
    original_url = url
    while True:
        tags_a = url_access(url, 'a')
        lst_url = [tag.get("href", None) for tag in tags_a if tag.contents[0]=="next"]
        try:
            url = re.findall("(\S*)index.html", original_url)[0]+lst_url[0]
        except:
            break
        print("Accessing url:", url)
        get_info(url)
    conn.commit()
print("Done")
