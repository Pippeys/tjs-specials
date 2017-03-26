#python3
#https://www.alltrails.com/us/california/backpacking scraping for locations

from bs4 import BeautifulSoup
import urllib
import requests

trail_soup = BeautifulSoup(open("https://www.alltrails.com/us/california/backpacking"))
print (soup.prettify())
trail_sauce = trail_soup.fina_all('a')
