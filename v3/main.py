import csv
import re
from utils import get_star_elements, get_soup, is_last_page, get_key 
import os





# Reset all formatting
RESET = "\033[0m"

# Colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Example usage

hash = {}
page_number = 1
file_name = './data.csv' 
if os.path.isfile(file_name):
    # File exists, proceed with reading and writing
    with open(file_name, "r") as file:
        reader = csv.reader(file, delimiter='|')
        existing_items = list(reader)
        for item in existing_items:
            title, image, *_ = item 
            if(get_key(title, image) not in hash):
                hash[get_key(title, image)] = item
            else:
                print(RED + 'The file is corrupt! It contains duplicate elements! Delete the file to continue!', RESET)

with open(file_name, "a") as file:
    writer = csv.writer(file, delimiter='|')
    while True:
        page = get_soup(page_number)
        elements = get_star_elements(page) 
        print(YELLOW + f"Found {len(elements)} products in page {page_number}." + RESET)
        for index, element in enumerate(elements):
            item = element.parent.parent.parent.parent.parent.parent.parent.parent.parent
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

            if(get_key(title, image) not in hash):
                print(BLUE + f"Found new item, {title}." + RESET)
                hash[get_key(title, image)] = [ title, image, rating, number_of_reviews]
                writer.writerow([ title, image, rating, number_of_reviews])

        if(is_last_page(page)):
            break
        page_number += 1
