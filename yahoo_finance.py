import urllib.request
import ssl
from bs4 import BeautifulSoup as bs

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input("Enter url: ")
data = urllib.request.urlopen(url, context=ctx).read()
html = bs(data, "html.parser")

info_dict = {'Current price': ['div', ('data-reactid', '31')],
           'Previous Close': ['td', ('data-reactid', '41')],
           'Open':['td', ('data-reactid', '46')],
           'Volume': ['td', ('data-reactid', '51')],
           "Day's Range": ['td', ('data-reactid', '59')],
           '52 Week Range': ['td', ('data-reactid', '63')],
           'Avg.Volume': ['td', ('data-reactid', '67')]}

def get_info(info):
    tags = html(info_dict[info][0])
    for tag in tags:
        attr = tag.attrs
        if info_dict[info][1] in attr.items(): return tag.text
while True:
    info = input('Type the info:')
    if info == '': break
    try:
        print(info, get_info(info))
    except:
        print('Invalid input')
