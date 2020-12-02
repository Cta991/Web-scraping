from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Path to chromedriver
DRIVER_PATH = 'C:/Users/Admin/Desktop/Python/Practice/Web scraping/chromedriver.exe'

#Options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = True
options.add_argument('--ignore-certifiacte-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

#Get the pass from a local txt file

#Login to facebook
url = "https://www.facebook.com/"
driver.get(url)

username_box = driver.find_element_by_id('email')
username_box.send_keys(USERNAME)

password_box = driver.find_element_by_id('pass')
password_box.send_keys(password)

login_box = driver.find_element_by_name('login')
login_box.click()
print('Logging into Facebook...')
time.sleep(10)
#Check for new ib
try:
    mess_new_ib = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[2]/div[4]/div[1]/div[2]/span/div/div[2]/span/span')
    new_ib_num = mess_new_ib.text
    ib = 'New ib: ' + new_ib_num + '\n'
except:
    new_ib_num = '0'
    ib = 'No new message\n'
driver.close()

i=0
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
url = "https://www.messenger.com/"
driver.get(url)

#Login to messenger
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
username_box = driver.find_element_by_xpath('//*[@id="email"]')
username_box.send_keys(USERNAME)

password_box = driver.find_element_by_xpath('//*[@id="pass"]')
password_box.send_keys(password)

login_box = driver.find_element_by_name('login')
login_box.click()
print('Logging into Messenger...')
time.sleep(10)
#Get the html for the messages box
try:
    list_ib = driver.find_elements_by_tag_name('ul')
    html = list_ib[0].get_attribute('innerHTML')
    soup = bs(html, "html.parser")
    driver.close()
    #Loop through the box
    if True:
        tags_li = soup('li')
        for item in tags_li:
            list_attr = [item2.attrs for item2 in item.find_all('div')]
            if {'class': ['accessible_elem']} in list_attr: continue
            Time = item.find_all('abbr')[0].text
            for item3 in item.find_all('span'):
                if item3.attrs == {'class': ['_1ht6', '_7st9']}:
                    ib += ('Name: ' + item3.text + '\n')
                elif item3.attrs == {'class': ['_1htf', '_6zke']}:
                    ib += ('Text: ' + item3.text + '\n')
                    ib += ('Time: ' + Time + '\n')
                else: continue
            ib += ('===============\n')
            i+=1
            if i == 5: break
except:
    ib += 'Error...'
    driver.close()

# set up the SMTP server
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('cuong.bot.72@gmail.com', 'khca18111999')

sender = 'cuong.bot.72@gmail.com'
receiver = 'ttcuong18111999@gmail.com'

# Create message container
msg = MIMEMultipart()
msg['Subject'] = "New messages"
msg['From'] = sender
msg['To'] = receiver

# add in the message body
msg.attach(MIMEText(ib, 'plain'))

# send the message via the server set up earlier.
s.send_message(msg)
s.quit()
print('Done')
