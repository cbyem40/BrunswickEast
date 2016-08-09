import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import csv


print "-----------------------------------------"
print "Look for price in PCHOME."
print "Start!"
print ""

# read csv file
with open('input_pchome_item_list.csv', 'rb') as f:
    reader = csv.reader(f)
    item_list = list(reader)

output = list()

for items in item_list:

  item_result = list()
  
  # get content in the csv file
  item = items[1]
  rt_item_no = items[0]

  # prepare the request to pchome
  url = "http://ecshweb.pchome.com.tw/search/v3.3/all/results?q=" + item + "&page=1&sort=rnk/dc" 
  res = requests.get(url)
  item_info = json.loads(res.text)
  
  item_count = len(item_info["prods"])
  item_name = item_info["prods"][0]["name"]
  item_price = item_info["prods"][0]["price"]
  item_id = item_info["prods"][0]["Id"]

  print "item_no: " , item
  if (item_count >1 ): 
    print url
    print "size: ", item_count
    print item_name, ",", item_id, ",", "$", item_price
    print " "
  else:
    print item_info["prods"][0]["name"],",",item_info["prods"][0]["Id"],",","$",item_info["prods"][0]["price"]
    print " "
  
  item_result = [rt_item_no,item,item_name,item_price,item_count,url]
  output.append(item_result)

with open('output_pchome_price.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(output)

print "Done. "
print ""

# rt_item_no, pchome_item_no, item_name, price, size, url


