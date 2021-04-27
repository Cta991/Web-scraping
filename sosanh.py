from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import time
import random

#Set up ChromeDriver
DRIVER_PATH = 'C:/Users/Admin/Desktop/Python/Practice/Web scraping/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options, executable_path = DRIVER_PATH)

#Ask for book name
book_name = input('What do you want to search for? ')
#book_name = 'Em se den cung con mua'
#Search on nhanam
url = 'http://nhanam.com.vn/'
driver.get(url)
search_box = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/form/input[1]')
search_box.send_keys(book_name)
search_button = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/form/input[2]')
search_button.click()
time.sleep(5)
html = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/ul')
book_list = html[0].get_attribute('innerHTML')
soup = bs(book_list, 'html.parser')
books = soup.find_all('div', class_='popup')
print('Number of books available:', len(books))
for book in books:
    name1 = book.find_all('h1', class_='name')[0].text.strip()
    price1 = book.find_all('p', class_='price')[0].text.strip().split('đ')[0]
    print(name1, price1)

#Search on tiki
url = 'https://tiki.vn/'
driver.get(url)
search_box = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/header/div[1]/div/div[1]/div[2]/div/input')
search_box.send_keys(book_name)
search_button = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/header/div[1]/div/div[1]/div[2]/div/button')
search_button.click()
time.sleep(5)
html = driver.find_elements_by_xpath('//*[@id="__next"]/div[1]/main/div[2]/div/div[2]/div/div[2]/a[1]/span')
book_list = html[0].get_attribute('innerHTML')
soup = bs(book_list, 'html.parser')
name2 = soup.find_all('div', class_='name')[0].text.strip()
price2 = soup.find_all('div', class_='price-discount')[0].text.strip()
print(name2, price2)

#Search on fahasa
url = 'https://www.fahasa.com/?attempt=1'
driver.get(url)
search_box = driver.find_element_by_xpath('//*[@id="search_desktop"]')
search_box.send_keys(book_name)
search_button = driver.find_element_by_xpath('//*[@id="search_mini_form_desktop"]/div/div/span')
search_button.click()
time.sleep(5)
html = driver.find_elements_by_xpath('//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[5]/div[2]/ul/li[1]/div')
book_list = html[0].get_attribute('innerHTML')
soup = bs(book_list, 'html.parser')
name3 = soup.find_all('h2', class_='product-name-no-ellipsis p-name-list')[0].text.strip()
price3 = soup.find_all('span', class_='price')[0].text.strip()
print(name3, price3)

driver.close()
