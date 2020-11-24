from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import re

DRIVER_PATH = 'C:/Users/Admin/Desktop/New folder/chromedriver.exe'

options = webdriver.ChromeOptions()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument("--window-size=1920,1200")
options.add_argument("--ignore-certificate-errors")
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
url = input("Enter url: ")
driver.get(url)
data = driver.page_source
html = bs(data, 'html.parser')

tags_a = html('a')
lst_info = []
for tag in tags_a:
    attr = tag.attrs
    if ('class', ['product-item']) in attr.items():
        info = tag.text
        print(info)
        try:
            Discount = re.findall('(-[0-9]*%)', info)[0]
        except:
            Discount = '0%'
        Price = re.findall('([0-9]*\.[0-9]*)', info)[0]
        Review_num = re.findall('(\([0-9]*\))', info)[0]
        Name = info.split(Review_num)[0]
        dict = {}
        dict['Name'] = Name
        dict['Review_num'] = Review_num
        dict['Price'] = Price
        dict['Discount'] = Discount
        lst_info.append(dict)
