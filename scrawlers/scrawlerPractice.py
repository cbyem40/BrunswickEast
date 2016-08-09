import requests
from bs4 import BeautifulSoup

response = requests.get('http://ecshweb.pchome.com.tw/search/v3.3/?q=%E8%88%92%E6%BD%94%20110&scope=all&sortParm=prc&sortOrder=ac')

soup = BeautifulSoup(response.text)
# items = soup.find_all(class='col3f')   
# soup.select('#ItemContainer')
#for item in items:
#    print item.select('.price') 

items = soup.select('.c3f')
print response.text 
