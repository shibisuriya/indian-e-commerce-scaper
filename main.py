#Scaper works as on Sep 3 2021

import requests
from bs4 import BeautifulSoup
# Setting the useragent so that Amazon.in doesn't drop our http requests.
headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}

# collect keywork from the user for scraping appropriate products from amazon.in.
page = requests.get(
    'https://www.amazon.in/s?k=gaming+keyboard&ref=nb_sb_noss_2', headers=headers)
soup = BeautifulSoup(page.content, 'html5lib') 

#HTML elements whose class attribute is set to 'a-icon-alt' are the elements where the star rating of a product is stored.
products = soup.find_all(class_="a-icon-alt")
for product in products:
    #Eliminate the HTML elements which are used by the users to filter products based on star rating, these elements also have
    #their class attribute set to "a-icon-alt". We are not interested in these elements because they are part of the panel which let's
    #users sort products based on availablity, features, brand etc. These element's parent don't have any product associated with them.
    if('&' not in str(product)):
        print(product)
