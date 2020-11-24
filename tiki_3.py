from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import sqlite3

DRIVER_PATH = 'C:/Users/Admin/Desktop/Python/Practice/Web scraping/chromedriver.exe'

options = webdriver.ChromeOptions()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--ignore-certificate-errors")
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
url = input("Enter url: ")
driver.get(url)
print('Accessing:', url)
data = driver.page_source
html = bs(data, 'html.parser')
driver.quit()

def check_tag(info, tag):
    return ('class', [info]) in tag.attrs.items()

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

tags_a = html('a')
lst_info = []
for tag in tags_a:
    if check_tag('product-item', tag):
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

print("Done")
