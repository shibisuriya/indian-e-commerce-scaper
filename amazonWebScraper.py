# Scraper works as on Sep 3 2021
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
from argparse import RawTextHelpFormatter
import os
import random
from debugger import writeEntirePage
from headers import headers

# Parsing commandline arguments.
parser = argparse.ArgumentParser(
    prog='amazonWebScaper', description='''Scrape products from wwww.amazon.in and sort them based on \'number of reviews\', \'start rating\', \'price\',  etc. \nSupports both wizard mode and command line mode.''',
    epilog='Happying shopping! :)\nWritten by https://www.github.com/shibisuriya', formatter_class=RawTextHelpFormatter)
parser.add_argument('-d', '--debugger', action='store_true',
                    help='''Send all scraped pages to the debugger (debugger writes the HTML pages sent to it in the folder ./DebuggerOutput after some processing like \nremoving nav bar, footer, highlighting the starElements, etc. These HTML pages can then be used by users to debug the script).''')

parser.add_argument('-dz', '--debugger-zero', action='store_true',
                    help='''Send pages which contain zero starElements to the debugger (debugger writes the HTML pages sent to it in the folder ./DebuggerOutput after \nsome processing like removing nav bar, footer, highlighting the starElements, etc. These HTML pages can then be used by users to debug the script).''')

parser.add_argument('-t', '--delay', nargs=2, metavar=('min_sec', 'max_sec'), type=int,
                    help='''Introduce random delays between requests (This is to prevent Amazon.in from detecting that we are an internet bot). \nThe script will generate a random number \'x\' between min_sec and max_sec, and will introduce a delay of \'x\' seconds between requests.''')

parser.add_argument("-k", "--keyword", default=[], nargs='+',
                    help='''Enter one or more keywords. These keywords will be used to query Amazon.in, if your keywords have multiple words like 'mechanical keyboards'\nor 'gaming keyboard' then type them inbetween single or double quotes followed by white space.\nFor example, --keyword 'mechanical keyboard' "gaming keyboard" "keyboard"''')

parser.add_argument('-a', '--append', action="store_true",
                    help='''Append the results to output.csv, if this option is not used then the script will overwrite output.csv file.''')

parser.add_argument('-p', '--page', metavar='NUMBER_OF_PAGE', type=int,
                    help='''Enter the number of pages to scrape per keyword.''')

parser.add_argument('--rerun', metavar='NUMBER_OF_TIMES', type=int,
                    help='''Do you want to run the script multiple times? It is advised to run the script multiple\ntimes for the same keywords to scrape most if not all products from Amazon.''')

parser.add_argument('--batch', action='store_true',
                    help='''Avoid asking for user inputs (optional options), and use default options wherever possible. Used for non-interactive sessions or for scripting...''')

args = parser.parse_args()
print(args)

# enable debug mode?
enableDebugMode = args.debugger

if(args.append == True):
    productCollection = pd.read_csv('output.csv')
else:
    if os.path.getsize('output.csv') != 0:
        if(args.batch == True):
            print('output.csv is not empty! Do you want to overwrite it? (y / n) n')
            productCollection = pd.read_csv('output.csv')
        else:
            while True:
                overwriteChoice = str(
                    input('output.csv is not empty! Do you want to overwrite it? (y / n) '))
                if(overwriteChoice == 'y'):
                    productCollection = pd.DataFrame(
                        columns=['Name', 'IsSponsored', 'StarRating', "ReviewCount", "Timestamp"])
                    break
                elif(overwriteChoice == 'n'):
                    productCollection = pd.read_csv('output.csv')

# Collecting keywords from the user.
keyList = []
keyCount = 1
# Normal mode
if(len(args.keyword) == 0):
    print("Enter a list of keys: ")
    while True:
        key = str(input(str(keyCount) + ") "))
        if(key == ''):
            break
        else:
            if not all(chr.isalnum() or chr.isspace() for chr in key):
                print("The entered string contains not alphanumeric characters...")
            else:
                key = key.strip()
                key = key.replace(' ', '+')
                keyList.append(key)
                keyCount = keyCount + 1
# Command line mode
else:
    for key in args.keyword:
        if not all(chr.isalnum() or chr.isspace() for chr in key):
            parser.error('Keywords contain non alphanumeric characters...')
        else:
            key = key.strip()
            key = key.replace(' ', '+')
            keyList.append(key)
            keyCount = keyCount + 1

# Normal mode
if(args.page is None):
    totPages = int(input("Enter the number of pages you want to scrape: "))
# Command line mode
else:
    totPages = args.page

for key in keyList:
    for pageNumber in range(1, totPages + 1):
        url = 'https://www.amazon.in/s?k=' + key + \
            '&ref=nb_sb_noss_2&page=' + str(pageNumber)
        page = requests.get(
            url, headers=headers)
        soup = BeautifulSoup(page.content, 'html5lib')

        # HTML elements whose class attribute is set to 'a-icon-alt' are the elements where the star rating of a product is stored.
        products = soup.find_all(class_="a-icon-alt")

        uniqueProductCount = 0
        productFoundInPage = 0
        for product in products:
            # Eliminate the HTML elements which are used by the users to filter products based on star rating, these elements also have
            # their class attribute set to "a-icon-alt". We are not interested in these elements because they are part of the panel which let's
            # users sort products based on availablity, features, brand etc. These element's parent don't have any product associated with them.

            if('&' not in str(product)):
                productFoundInPage += 1
                timestamp = datetime.datetime.fromtimestamp(
                    time.time()).strftime('%d-%m-%Y %H:%M:%S %p')
                fullProduct = product.parent.parent.parent.parent.parent.parent.parent
                classAttr = fullProduct.get('class')
                if(set(['a-section', 'a-spacing-none']) <= set(classAttr)):
                    if(len(classAttr) > 2):
                        fullProduct = product.parent.parent.parent.parent.parent.parent

                # Find if product is sponsored or not.
                isSponsored = fullProduct.find(
                    class_="s-label-popover-default")
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

                # Find start rating of the product.
                starRating = fullProduct.find(class_='a-icon-alt')
                if(starRating):
                    starRating = starRating.text
                    starRating = starRating.split('out', 1)[0]
                    starRating = starRating.strip()

                else:
                    print("Unable to find starRating...")

                # Find review count of the product.
                # import pdb; pdb.set_trace()
                reviewCount = fullProduct.find(class_='a-color-link')
                if(reviewCount):
                    reviewCount = reviewCount.text
                    reviewCount = reviewCount.replace(',', '')
                    if(reviewCount.isnumeric() == False):
                        print("reviewCount is a string")

                else:
                    reviewCount = fullProduct.find(class_='a-size-base')
                    if(reviewCount):
                        reviewCount = reviewCount.text
                        reviewCount = reviewCount.replace(',', '')
                        if(reviewCount.isnumeric() == False):
                            print("String in reviewCount")
                    else:
                        print("Unable to find reviewCount...")

                productJson = {
                    "Name": name,
                    "IsSponsored": isSponsored,
                    "StarRating": starRating,
                    "ReviewCount": reviewCount,
                    "Timestamp": timestamp
                }

                if(not name in productCollection.values):
                    productCollection = productCollection.append(
                        productJson, ignore_index=True)
                    uniqueProductCount += 1

                # Introduce random delay between requests.

        # Give user the option to send page to the debugger function when the script finds 0 star element in the html.
        # Sometimes amazon.in detects that we are a bot and it drops our requests.
        fileName = timestamp + " - " + url + ".html"
        if(enableDebugMode == False and productFoundInPage == 0):
            while True:
                userChoice = str(input(
                    "0 star elements found in the page. Do you want to send this page to the debugger? (y/n) "))
                if(userChoice == 'y'):
                    writeEntirePage(fileName, soup, productFoundInPage,
                                    uniqueProductCount, len(products), url)
                    break
                elif(userChoice == 'n'):
                    break
                else:
                    print("Invalid input entered. Please enter y or n...")

        if(enableDebugMode == True):
            writeEntirePage(fileName, soup, productFoundInPage,
                            uniqueProductCount, len(products), url)
        print("Found ", productFoundInPage, " products in ", url,
              " out of which ", uniqueProductCount, " are new.")

        # Avoid time delay for last page
        if(args.delay is not None and pageNumber < totPages):
            randomNumber = random.randint(args.delay[0], args.delay[1])
            time.sleep(randomNumber)

print(productCollection)
productCollection.to_csv('output.csv', index=False)
