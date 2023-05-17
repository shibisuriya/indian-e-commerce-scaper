import csv
import re
from utils import get_star_elements, get_soup, is_last_page, get_key, get_item_from_star_element
import os
from print import print_yellow, print_blue, print_red


hash = {}
page_number = 1
file_name = './data.csv' 
does_file_exists = bool(os.path.isfile(file_name))
if does_file_exists:
    with open(file_name, "r") as file:
        reader = csv.reader(file, delimiter='|')
        existing_items = list(reader)
        for item in existing_items:
            title, image, *_ = item 
            key = get_key(title, image) 
            if(key not in hash):
                hash[key] = item
            else:
                print_red('The file is corrupt! It contains duplicate elements! Delete the file and re-run the script!')
                exit()

with open(file_name, "a") as file:
    writer = csv.writer(file, delimiter='|')
    # write header, since the file is new.
    if not does_file_exists: 
        print_blue("File doesn't exist, created a new file!")
        writer.writerow(['title', 'image', 'rating', 'number of reviews'])
    while True:
        page = get_soup(page_number)
        elements = get_star_elements(page) 
        print_yellow(f"Found {len(elements)} products in page {page_number}.")
        for index, element in enumerate(elements):
            item = get_item_from_star_element(element) 
            image = item.find('img', class_='s-image') 
            if(image):
                image = image['src']

            title = item.find('span', class_='a-size-base-plus a-color-base a-text-normal') 
            if(title):
                title = title.text
            else: 
                title = item.find('span', class_="a-size-medium a-color-base a-text-normal") 
                title = title.text
            
            rating = item.find('span', class_='a-icon-alt').text
            rating = re.search(r'(.+?) out', rating).group(1).strip()

            number_of_reviews = item.find('span', class_="a-size-base s-underline-text").text

            key = get_key(title, image) 
            if(key not in hash):
                print_blue(f"Found new item, {title}.")
                hash[key] = [ title, image, rating, number_of_reviews]
                writer.writerow([ title, image, rating, number_of_reviews])

        if(is_last_page(page)):
            break
        page_number += 1
