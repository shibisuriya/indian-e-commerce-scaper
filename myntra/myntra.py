import requests
import json
import csv
from utils import get_cookies, get_headers;

def get_rows():
    return 50

def get_params(p = 1): 
    o = '0'
    rows = get_rows()
    if(p == 1): 
        o = '0'
    else:
        o = str((p - 1 ) * rows - 1)
    params = {
        'f': 'Gender:men,men women',
        'p': str(p),
        'o': o,   
        'rows': str(rows),
        'plaEnabled': 'false',
        'xdEnabled': 'false',
        'pincode': '',
    }
    if(p == 1):
        del params['p']
    return params


def get_total_pages():
    response = make_request()
    totalCount = response['totalCount']
    rows = get_rows()
    if(totalCount % rows == 0):
        return int(totalCount / rows) 
    else:
        return int(totalCount / rows) + 1 

def get_key(): 
    return 't-shirt'

def make_request(p = 1):
    cookies = get_cookies()
    headers = get_headers()
    params = get_params(p)
    key = get_key()
    print('key -> ', key, ' params -> ', params)
    response = json.loads(requests.get('https://www.myntra.com/gateway/v2/search/' + key, params=params, cookies=cookies, headers=headers).text)
    return response

def get_products(p = 1):
    response = make_request(p)
    return response['products']

unique_product_ids = set()
unique_products = []
non_unique_products = []
total_pages = get_total_pages()
for i in range(1, total_pages+1):
    products = get_products(i)
    for product in products:
        if product["productId"] not in unique_product_ids:
            unique_product_ids.add(product["productId"])
            unique_products.append(product)
        else: 
            non_unique_products.append(product)

fieldnames = ["productId", "productName", "price", "rating", "ratingCount", "searchImage"]
with open("unique-products.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product in unique_products:
        row = {key: product[key] for key in fieldnames}
        writer.writerow(row)


with open("non-unique-products.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product in non_unique_products:
        row = {key: product[key] for key in fieldnames}
        writer.writerow(row)

