import requests
from bs4 import BeautifulSoup
from urllib import request
import urllib
import re

id = input('a: ')
req = requests.get('http://www.tan8.com/codeindex.php?d=web&c=weixin&m=piano&id={}&isalbum=0'.format(id))
html = req.text
bf = BeautifulSoup(html, 'html.parser')
text = bf('div', class_='author_text').children
person = text
print(person)