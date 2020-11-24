from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import sqlite3

#Retrieve the data
DRIVER_PATH = 'C:/Users/Admin/Desktop/Python/Practice/Web scraping/chromedriver.exe'

options = webdriver.ChromeOptions()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--ignore-certificate-errors")
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

#Set up the database
conn = sqlite3.connect('tiki.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Books;
CREATE TABLE Books (
    Name TEXT,
    Review_num TEXT,
    Discount TEXT,
    Price TEXT
);
''')

#A function that check a specific class inside a tag
def check_tag(info, tag):
    return ('class', [info]) in tag.attrs.items()

#Loop through the pages
i=1
while True:
    url = "https://tiki.vn/nha-sach-tiki/c8322?page=" + str(i)
    try:
        driver.get(url)
    except:
        break
    print("Accessing URL:", url)
    data = driver.page_source
    html = bs(data, 'html.parser')
    tags_a = html('a')
    book_count=0
    for tag in tags_a:
        if check_tag('product-item', tag):
            book_count+=1
            for item in tag.find_all('div'):
                if check_tag('info', item):
                    for item_2 in item.find_all('div'):
                        if check_tag('name', item_2): Name = item_2.text
                        elif check_tag('rating-review', item_2): Review_num = item_2.text
                        elif check_tag('price-discount__price', item_2): Price = item_2.text
                        elif check_tag('price-discount__discount', item_2): Discount = item_2.text
                    cur.execute('''INSERT INTO Books (Name, Review_num, Discount, Price)
                                VALUES (?,?,?,?)''', (Name, Review_num, Discount, Price))
                    Discount = "0%"
                    conn.commit()
    print('There are',book_count,'books in page', i, '.')
    i+=1

driver.close()
print("Done")
