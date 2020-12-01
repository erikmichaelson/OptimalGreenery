import requests
from bs4 import BeautifulSoup
from lxml import html
import webbrowser

urlbase = 'https://www.zillow.com/homes/'
urlfull = 'https://www.zillow.com/homes/4200-Sunnyside-rd-Edina,-MN,-55424_rb'
#address = address.replace
addresses = ['4200 Sunnyside rd Edina, MN, 55424', '4520 W 56th st Edina, MN, 55424']
prices = []
for add in addresses:
	add = add.replace(' ', '-')
	print(add)
	url = urlbase+ add+ '_rb'
	print(url)
	page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

	soup = BeautifulSoup(page.text, 'html.parser')

	price = soup.find(class_='zestimate-value')
	print(price.string)
	prices.append(price.string)
