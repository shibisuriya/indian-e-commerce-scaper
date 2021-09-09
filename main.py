# Scraper works as on Sep 3 2021
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
    prog='amazonWebScaper', description='''Scrape products from wwww.amazon.in and sort them based on \'number of reviews\', \'start rating\', \'price\',  etc.''',
    epilog='Happying shopping! :)\nWritten by https://www.github.com/shibisuriya', formatter_class=RawTextHelpFormatter)
parser.add_argument('-d', '--debugger', action='store_true',
                    help='''Send all scraped pages to the debugger (debugger writes the HTML pages sent to it in the folder ./DebuggerOutput after some processing like \nremoving nav bar, footer, highlighting the starElements, etc. These HTML pages can then be used by users to debug the script.)''')

parser.add_argument('-dz', '--debugger-zero', action='store_true',
                    help='''Send pages which contain zero starElements to the debugger (debugger writes the HTML pages sent to it in the folder ./DebuggerOutput after \nsome processing like removing nav bar, footer, highlighting the starElements, etc. These HTML pages can then be used by users to debug the script.)''')

parser.add_argument('-t', '--delay', nargs=2, metavar=('min_sec', 'max_sec'), type=int,
                    help='''Introduce random delays between requests (This is to prevent Amazon.in from detecting that we are an internet bot). \nThe script will generate a random number \'x\' between min_sec and max_sec, and will introduce a delay of \'x\' seconds between requests.''')

parser.add_argument("-k", "--keyword", default=[], nargs='+',
                    help='''Enter one or more keywords. These keywords will be used to query Amazon.in, if your keywords have multiple words like 'mechanical keyboards'\nor 'gaming keyboard' then type them inbetween single or double quotes followed by white space.\nFor example, --keyword 'mechanical keyboard' "gaming keyboard" "keyboard"''')

parser.add_argument('-a', '--append', action="store_true",
                    help='''Append the results to output.csv, if this option is not used then the script will overwrite output.csv file.''')

args = parser.parse_args()
print(args)

# enable debug mode?
if(args.debugger == True):
    print("debugger is one")
    # Write entire page
    # Clear debugger file
    entirePageFile = open("debugger_output.html", "w")
    entirePageFile.write(
    "<style> \
        .fullPage {border-left: 90px solid green; border-right: 90px solid green; max-width: 100%; margin: 2em auto;} \
        .s-desktop-width-max1 {max-width: 100%;} \
        .a-icon-alt-red {border: 5px solid red; margin: 2px; padding: 2px;} \
        .a-icon-alt-green {border: 5px solid #00FF00; margin: 2px; padding: 2px;} \
        .pageInformation {border: 3px solid black; color: white; margin: 0 auto; max-width: 100%; background-color: black; padding: 1.2em; font-size: 1.5em;} \
        .badge-red {background-color: red; border: 1px solid black; color: white; font-size:2em;border-radius:1em;} \
        .badge-green {background-color: green; border: 1px solid black; color: white; font-size:2em;border-radius:1em;} \
        .pageInformationChild {margin: 1em;} \
    </style>")


def writeEntirePage(soup, productFoundInPage, uniqueProductCount, totalStarElementFoundInpage, url):
    entirePageFile.write('<div class="pageInformation">')
    entirePageFile.write("<div class='pageInformationChild'>Total StarElements found in page = " +
                         str(totalStarElementFoundInpage) + " </div>")
    entirePageFile.write(
        "<div class='pageInformationChild'>Valid products found in page = " + str(productFoundInPage) + " </div>")
    entirePageFile.write(
        "<div class='pageInformationChild'>URL = " + str(url) + " </div>")
    entirePageFile.write("</div>")

    # Remove unwanted elements.
    soup.find("header", {"id": "navbar-main"}).decompose()
    soup.find("div", {"id": "navFooter"}).decompose()
    soup.find(class_="a-dropdown-container").decompose()
    soup.find(id="skiplink").decompose()

    soup.find(
        class_="s-desktop-width-max s-desktop-content s-opposite-dir sg-row")['class'] = "s-desktop-width-max1 s-desktop-content s-opposite-dir sg-row"
    icons = soup.find_all(class_='a-icon-alt')
    for index, icon in enumerate(icons):
        if('&' not in str(icon)):
            badge = soup.new_tag('span', attrs={"class": "badge-green"})
            badge.string = str(index + 1)
            icon.parent.parent['class'] = 'a-icon-alt-green'
            icon.parent.append(badge)

        else:
            badge = soup.new_tag('span', attrs={"class": "badge-red"})
            badge.string = str(index + 1)
            icon.parent.parent['class'] = 'a-icon-alt-red'
            icon.parent.parent.parent.append(badge)

    # print(icons)

    entirePageFile.write('<div class="fullPage">')
    entirePageFile.write(soup.prettify())
    entirePageFile.write("</div>")


# collect keywords from the user for scraping appropriate products from amazon.in.
while True:
    appendDataFrame = str(
        input("Do you want to append the results to the existing .csv file? (y/n) "))
    if(appendDataFrame == 'y'):
        productCollection = pd.read_csv('output.csv')
        break
    elif(appendDataFrame == 'n'):
        productCollection = pd.DataFrame(
            columns=['Name', 'IsSponsored', 'StarRating', "ReviewCount", "Timestamp"])
        break
    else:
        print("Invalid character entered, please enter y or n.")
        continue

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
                    time.time()).strftime('%d-%m-%Y %H:%M:%S')
                fullProduct = product.parent.parent.parent.parent.parent.parent.parent
                classAttr = fullProduct.get('class')
                if(set(['a-section', 'a-spacing-none']) <= set(classAttr)):
                    if(len(classAttr) > 2):
                        fullProduct = product.parent.parent.parent.parent.parent.parent
                        foundProduct(str(fullProduct), classAttr)

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
                # import pdb; pdb.set_trace()
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
                            foundError(str(fullProduct),
                                       "String in reviewCount")
                    else:
                        print("Unable to find reviewCount...")
                        foundError(str(fullProduct), "reviewCount")

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

        # Give user the option to send page to the debugger function when the script finds 0 star element in the html.
        # Sometimes amazon.in detects that we are a bot and it drops our requests.
        if(enableDebugMode == False and productFoundInPage == 0):
            while True:
                userChoice = str(input(
                    "0 star elements found in the page. Do you want to send this page to the debugger? (y/n) "))
                if(userChoice == 'y'):
                    writeEntirePage(soup, productFoundInPage,
                                    uniqueProductCount, len(products), url)
                    break
                elif(userChoice == 'n'):
                    break
                else:
                    print("Invalid input entered. Please enter y or n...")

        if(enableDebugMode == True):
            writeEntirePage(soup, productFoundInPage,
                            uniqueProductCount, len(products), url)
        print("Found ", productFoundInPage, " products in ", url,
              " out of which ", uniqueProductCount, " are new.")
print(productCollection)
productCollection.to_csv('output.csv', index=False)
