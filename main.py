# Scraper works as on Sep 3 2021
from os import stat_result
import requests
from bs4 import BeautifulSoup
import pandas as pd

# collect keywork from the user for scraping appropriate products from amazon.in.
productCollection = pd.DataFrame()
keyList = []
print("Enter a list of keys: ")
keyCount = 1
while True:
    key = str(input(str(keyCount) + ") "))
    if(key == ''):
        break
    else:
        if not all(chr.isalnum() or chr.isspace() for chr in key):
            print("The entered string contains not alphanumeric characters...")
        else:
            key = key.replace(' ', '+')
            keyList.append(key)
            keyCount = keyCount + 1
settingsFile = open('settings.cfg', 'w+')
settingsJson = settingsFile.read()
print(settingsJson)
if(settingsJson == ''):
    print("Empty!")
settingsFile.write(str(keyList))
exit()

f = open("output.html", "w")
h = open("full.html", "w")

f.write(
    "<style>.product{border: 2px solid red; padding: 1em; margin: 1em;}</style>")
h.write(
    "<style>.product{border: 2px solid red; padding: 1em; margin: 1em;}</style>")


def foundError(data, name):
    f.write("<div class='product'><h2>" + name + "</h2>")
    f.write(data)
    f.write("</div>")


def foundProduct(data, classValue):
    h.write("<div class='product'>")
    for i in classValue:
        h.write("<h2>"+i+"</h2>")
    h.write(data)
    h.write("</div>")


# Setting the useragent so that Amazon.in doesn't drop our http requests.
headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}



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
            classAttr = fullProduct.get('class')
            if(set(['a-section', 'a-spacing-none']) <= set(classAttr)):
                if(len(classAttr) > 2):
                    fullProduct = product.parent.parent.parent.parent.parent.parent
                    foundProduct(str(fullProduct), classAttr)

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
                    name = fullProduct.find(
                        class_="a-truncate-full")
                    if(name):
                        name = name.text
                    else:
                        print("Failed to extract products contact developer...")
                        foundError(str(fullProduct), "name")

            # Find start rating of the product.
            starRating = fullProduct.find(class_='a-icon-alt')
            if(starRating):
                starRating = starRating.text
                starRating = starRating.split('out', 1)[0]
                starRating = starRating.strip()

            else:
                print("Unable to find starRating...")
                foundError(str(fullProduct), "starRating")

            # Find review count of the product.
            #import pdb; pdb.set_trace()
            reviewCount = fullProduct.find(class_='a-color-link')
            if(reviewCount):
                reviewCount = reviewCount.text
                reviewCount = reviewCount.replace(',', '')
                if(reviewCount.isnumeric() == False):
                    foundError(str(fullProduct), "String in reviewCount")
            else:
                reviewCount = fullProduct.find(class_='a-size-base')
                if(reviewCount):
                    reviewCount = reviewCount.text
                    reviewCount = reviewCount.replace(',', '')
                    if(reviewCount.isnumeric() == False):
                        foundError(str(fullProduct), "String in reviewCount")
                else:
                    print("Unable to find reviewCount...")
                    foundError(str(fullProduct), "reviewCount")

            productJson = {
                "name": name,
                "isSponsored": isSponsored,
                "starRating": starRating,
                "reviewCount": reviewCount
            }

            if(not name in productCollection.values):
                productCollection = productCollection.append(
                    productJson, ignore_index=True)

print(productCollection)
productCollection.to_csv('output.csv', index=False)
