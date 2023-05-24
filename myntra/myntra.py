import csv
import os
from utils import get_hash_key, get_products, get_total_pages

# Check if the data file already exists? 
file_name = './data.csv'
hash = {}
if os.path.isfile(file_name):
    print(f"{file_name} exists! Reading items from {file_name}!")
    # If the file already exists, then load all the items into the hash.
    with open(file_name, 'r') as file:
          csv_reader = csv.reader(file, delimiter='|')
          for item in csv_reader:
            id, name, *_ = item 
            hash_key = get_hash_key(id, name)
            if(hash_key not in hash): 
                hash[hash_key] = item
            else:
                print(f"{file_name} is corrupt! Duplicate entries found, please delete the file and re-run then script.")
                print(f'Duplicate item: {item}')
                exit()
else:
    print(f"{file_name} does not exist, creating a new file!")

with open(file_name, "a") as file:
    writer = csv.writer(file, delimiter='|')
    if(not os.path.isfile(file_name)):
        # Since the file is new, write the header... 
        field_names = ["productId", "productName", "price", "rating", "ratingCount", "searchImage", "landingPageUrl"]
        writer.writerow(field_names)
    total_pages = get_total_pages()
    for i in range(1, total_pages + 1):
        products = get_products(i)
        for product in products:
            productId = product['productId']
            landingPageUrl = product['landingPageUrl']
            productName = product['productName']
            price = product['price']
            rating = product['rating']
            searchImage = product['searchImage']
            ratingCount = product['ratingCount']
            hash_key = get_hash_key(productId, productName)
            if(hash_key not in hash): 
                print(f"Unique product found! {productName}.")
                fields = [productId, productName, price, rating, ratingCount, searchImage, landingPageUrl]
                hash[hash_key] = fields 
                writer.writerow(fields)



