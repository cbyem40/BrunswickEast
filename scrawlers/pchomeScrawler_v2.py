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
output.append(["rt_itemNo", "pchome_itemNo", "name", "price","found records", "url"])
line_count = 1 

for items in item_list:
  
  # skip the title line
  if (line_count == 1):
    line_count = line_count + 1
    continue
  line_count = line_count + 1


  item_result = list()
  
  # get content in the csv file
  item = items[1]
  rt_item_no = items[0]

  # prepare the request to pchome
  url = "http://ecshweb.pchome.com.tw/search/v3.3/all/results?q=" + item + "&page=1,2&sort=prc/ac" 
  readable_url = "http://ecshweb.pchome.com.tw/search/v3.3/?q=" + item + "&scope=all&sortParm=prc&sortOrder=ac"
  res = requests.get(url)
  item_info = json.loads(res.text)
  print url
  item_count = len(item_info["prods"])
  
  pointer = 0
  item_pointer = 0 
  available_for_sale = True

  if (item_count == 0):
    item_price = "no matches"
  elif (item_count >=1):

    while True:    
      # break if every item in the list is not for sale
      if (item_count == pointer):
        available_for_sale = False
        break
      item_id = item_info["prods"][pointer]["Id"]
      stock_url = "http://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/button&id=" + item_id + "&fields=Id,Price,Qty,ButtonType"
      stock_res = requests.get(stock_url)
      stock_info = json.loads(stock_res.text)
      pointer = pointer + 1 
      if stock_info[0]["ButtonType"] == "ForSale":
        break
      
    item_pointer = pointer -1
    
    if (available_for_sale):
      item_name = item_info["prods"][item_pointer]["name"]
      item_price = "$" + str(item_info["prods"][item_pointer]["price"])
      item_id = item_info["prods"][item_pointer]["Id"]
    else:
      item_name = item_info["prods"][0]["name"] 
      item_price = "no stock"
      item_id = ""
    
  print "item_no: " , item
  if (item_count >1 ): 
    print readable_url
    print "size: ", item_count
    print item_name, ",", item_id, ",", item_price
    print " "
  elif (item_count == 1):
    print item_info["prods"][0]["name"],",",item_info["prods"][0]["Id"],",","$",item_info["prods"][0]["price"]
    print " "
  else:
    print "not available"
  
  item_result = [rt_item_no,item,item_name,item_price,item_count,readable_url]
  output.append(item_result)

with open('output_pchome_price.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(output)

print "Done. "
print ""

# rt_item_no, pchome_item_no, item_name, price, size, url


