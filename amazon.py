from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import time
import sqlite3

#Retrieve Driver path
DRIVER_PATH = 'C:/Users/Admin/Desktop/Python/Practice/Web scraping/chromedriver.exe'

#Options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

#Set up database
conn = sqlite3.connect('Amazon.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Gaming;
CREATE TABLE Gaming (
    Name TEXT,
    Review_num TEXT,
    Rating TEXT,
    Price TEXT,
    Link TEXT
);
''')
#Sth to help
def check_tag(info, tag):
    return ('class', info) in tag.attrs.items()

def get_price(url):
    driver.get(url)
    source = driver.page_source
    soup = bs(source, 'html.parser')
    return soup.select('span.a-size-base.a-color-price')[0].text.strip()

def get_next_page(url):
#    driver.get(url)
    next_page = driver.find_elements_by_class_name('a-last')
    link = next_page[0].get_attribute('innerHTML')
    soup = bs(link, 'html.parser')
    next_url = soup('a')[0].get('href', None)
    return 'https://www.amazon.com'+str(next_url)

#Retrieve data from Amazon
url = 'https://www.amazon.com/s?bbn=16225016011&rh=n%3A%2116225016011%2Cn%3A471304&dc&fst=as%3Aoff&pf_rd_i=16225016011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=03b28c2c-71e9-4947-aa06-f8b5dc8bf880&pf_rd_r=9V6AW0WNFDCJ7X2ZRZWR&pf_rd_s=merchandised-search-3&pf_rd_t=101&qid=1489016289&rnid=16225016011&ref=s9_acss_bw_cts_AEVNVIDE_T4_w'
i=0
while True:
    driver.get(url)
    print("Accessing page", i+1)
#Get next page url
    try:
        url = get_next_page(url)
#        print(url)
    except:
        break
#    print(next_page)

#Get data from the current page
    html = driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[2]')
    data = html[0].get_attribute('innerHTML')
    soup = bs(data, 'html.parser')


    gears = soup.find_all('div', class_='a-section a-spacing-medium')
    for gear in gears:
        link = 'https://www.amazon.com' + gear.find_all('a', class_='a-link-normal a-text-normal')[0].get('href', None)
        try:
            price = gear.select('span.a-offscreen')[0].text.strip()
        except:
            price = get_price(link)
#    print(price)
        name = gear.select('a.a-link-normal.a-text-normal')[0].text.strip()
#    print(name)
        rating = gear.find_all('span', class_='a-icon-alt')[0].text.strip()
        rating = rating.split()[0]+'/'+rating.split()[3]
#    print(rating)
        review_num = [tag.text for tag in gear.select('span.a-size-base') if tag.get('class')==['a-size-base']][0]
#    print(review_num)
        cur.execute('''INSERT INTO Gaming (Name, Review_num, Rating, Price, Link) VALUES
                        (?,?,?,?,?)''', (name, review_num, rating, price, link))
    conn.commit()

    i+=1
    if i%3==0: time.sleep(5)

driver.close()
