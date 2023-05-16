import csv
import re
from utils import get_star_elements
hash = {}
with open('./data.csv', "w") as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow(['title', 'image', 'rating', 'number of reviews'])
    elements = get_star_elements() 
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

        if(f"{title}-{image}" not in hash):
            hash[f"{title}-{image}"] = [ title, image, rating, number_of_reviews]
            writer.writerow([ title, image, rating, number_of_reviews])
        else:
            print(f"Item {title} already exists in the hash!")

