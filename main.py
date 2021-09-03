# Scraper works as on Sep 3 2021
from os import stat_result
import requests
from bs4 import BeautifulSoup
import pandas as pd
# Setting the useragent so that Amazon.in doesn't drop our http requests.
headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}

# collect keywork from the user for scraping appropriate products from amazon.in.
productCollection = pd.DataFrame()
totPages = int(input("Enter the number of pages you want to scrape: "))
for pageNumber in range(1, totPages + 1):
    page = requests.get(
        'https://www.amazon.in/s?k=gaming+keyboard&ref=nb_sb_noss_2&page=' + str(pageNumber), headers=headers)
    soup = BeautifulSoup(page.content, 'html5lib')

    # HTML elements whose class attribute is set to 'a-icon-alt' are the elements where the star rating of a product is stored.
    products = soup.find_all(class_="a-icon-alt")
    print("Found ", len(products), " products in page ", pageNumber)

    for product in products:
        # Eliminate the HTML elements which are used by the users to filter products based on star rating, these elements also have
        # their class attribute set to "a-icon-alt". We are not interested in these elements because they are part of the panel which let's
        # users sort products based on availablity, features, brand etc. These element's parent don't have any product associated with them.

        if('&' not in str(product)):
            fullProduct = product.parent.parent.parent.parent.parent.parent.parent

            # Find if product is sponsored or not.
            isSponsored = fullProduct.find(class_="s-label-popover-default")
            if(isSponsored):
                isSponsored = True
            else:
                isSponsored = False

            # Find product's name.
            name = fullProduct.find(
                class_="a-size-medium a-color-base a-text-normal")

            if(name):
                name = name.text
            else:
                name = fullProduct.find(
                    class_="a-size-base-plus a-color-base a-text-normal")
                if(name):
                    name = name.text
                else:
                    print("Failed to extract products contact developer...")

            # Find start rating of the product.
            starRating = fullProduct.find(class_='a-icon-alt')
            if(starRating):
                starRating = starRating.text

            # Find review count of the product.
            reviewCount = fullProduct.find(class_="a-size-base")
            if(reviewCount):
                reviewCount = reviewCount.text

            productJson = {
                "name": name,
                "isSponsored": isSponsored,
                "starRating": starRating,
                "reviewCount": reviewCount
            }
            productCollection = productCollection.append(
                productJson, ignore_index=True)

print(productCollection)
