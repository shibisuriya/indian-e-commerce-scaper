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
from verbose import verbosePrint
from headers import headers
import json
# Parsing commandline arguments.
parser = argparse.ArgumentParser(
    prog='amazonWebScaper', description='''Scrape products from wwww.amazon.in and sort them based on \'number of reviews\', \'start rating\', \'price\',  etc. \nSupports both wizard mode and command line mode.''',
    epilog='Happying shopping! :)\nWritten by https://www.github.com/shibisuriya', formatter_class=RawTextHelpFormatter)
parser.add_argument('-d', '--debugger', action='store_true',
                    help='''Send all scraped pages to the debugger (debugger writes the HTML pages sent to it in the folder ./DebuggerOutput after some processing like \nremoving nav bar, footer, highlighting the starElements, etc. These HTML pages can then be used by users to debug the script).''')
parser.add_argument('-dz', '--debugger-zero', action='store_true',
                    help='''Send pages which contain zero starElements to the debugger (debugger writes the HTML pages sent to it in the folder ./DebuggerOutput after \nsome processing like removing nav bar, footer, highlighting the starElements, etc. These HTML pages can then be used by users to debug the script).\nWhen the script finds 0 starElements in the scraped page most probably Amazon.in would have found out that we are an internet bot and would have sent\nus a HTML page with captcha in it or Amazon.in would have dropped our http request.''')
parser.add_argument('-t', '--delay', nargs=2, metavar=('min_sec', 'max_sec'), type=int,
                    help='''Introduce random delays between requests (This is to prevent Amazon.in from detecting that we are an internet bot). \nThe script will generate a random number \'x\' between min_sec and max_sec, and will introduce a delay of \'x\' seconds between requests. \nNote: 'min_sec' should be less than'max_sec'. ''')
parser.add_argument("-k", "--keywords", default=[], nargs='+',
                    help='''Enter one or more keywords. These keywords will be used to query Amazon.in, if your keywords have multiple words like 'mechanical keyboards'\nor 'gaming keyboard' then type them inbetween single or double quotes followed by white space.\nFor example, --keyword 'mechanical keyboard' "gaming keyboard" "keyboard"''')
parser.add_argument('-a', '--append', action="store_true",
                    help='''Append the results to output.csv, if this option is not used then the script will overwrite output.csv file.''')
parser.add_argument('-p', '--page', metavar='NUMBER_OF_PAGE', type=int,
                    help='''Enter the number of pages to scrape per keyword.''')
parser.add_argument('--rerun', metavar='NUMBER_OF_TIMES', type=int,
                    help='''Do you want to run the script multiple times? It is advised to run the script multiple\ntimes for the same keywords to scrape most if not all products from Amazon.''')
parser.add_argument('--batch', action='store_true',
                    help='''Avoid asking for user inputs (optional options), and use default options wherever possible. Used for non-interactive sessions or for scripting...''')
parser.add_argument('--use-settings-from-last-session', action='store_true',
                    help='''Use the settings used by the user in the most recent session. The script stores the command line arguements and other options used by the user\nin settings.cfg file before exiting properly. When this --use-settings-from-last-session is used the script loads the options and other\nsettings from settings.cfg file and applies it to the current session.''')
parser.add_argument('--verbose', action='store_true',
                    help='''Provide addition details as to what the script is doing, useful while debugging or testing.''')
args = parser.parse_args()
print(args)
verbose = args.verbose
# See if any other option is entered simultaneously with --use-settings-from-last-session
if(args.use_settings_from_last_session == True):
    used = args.append or args.batch or args.debugger or args.debugger_zero or args.verbose
    used = used or (args.delay is not None) or len(args.keywords) > 0 or (
        args.page is not None) or (args.rerun is not None)
    if(used):
        parser.error(
            'You cannot use the option --use-settings-from-last-session with any other option(s)...')
# Disable debugger_zero mode when debug mode is on. We don't want to log a single page twice.
enableDebugMode = args.debugger
enableZeroDebugMode = args.debugger_zero
if(enableDebugMode and enableDebugMode):
    enableZeroDebugMode = False
    verbosePrint(
        verbose, "--debugger_zero set to False since --debugger is True.", "Note")
if(args.append == True):
    productCollection = pd.read_csv('output.csv')
    verbosePrint("Opening output.csv to write results.", verbose, "Note")
elif(args.append == False):
    if os.path.getsize('output.csv') != 0:
        if(args.batch == True):
            print('output.csv is not empty! Do you want to overwrite it? (y / n) n')
            productCollection = pd.read_csv('output.csv')
        else:
            while True:
                overwriteChoice = str(
                    input('output.csv is not empty! Do you want to overwrite it? (y / n) '))
                if(overwriteChoice == 'y'):
                    print(
                        "Overwriting results present in output.csv with fresh results.")
                    productCollection = pd.DataFrame(
                        columns=['Name', 'IsSponsored', 'StarRating', "ReviewCount", "Timestamp"])
                    break
                elif(overwriteChoice == 'n'):
                    print('Appending fresh results to output.csv')
                    productCollection = pd.read_csv('output.csv')
                    break
                else:
                    print('Invalid choice entered. Please type y or n...')
    else:
        productCollection = pd.DataFrame()
# Collecting keywords from the user.
keyList = []
keyCount = 1
# Normal mode
if(len(args.keywords) == 0):
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
    for key in args.keywords:
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
        timestamp = ''
        for product in products:
            # Eliminate the HTML elements which are used by the users to filter products based on star rating, these elements also have
            # their class attribute set to "a-icon-alt". We are not interested in these elements because they are part of the panel which let's
            # users sort products based on availablity, features, brand etc. These element's parent don't have any product associated with them.
            # These control elements look like this <span class="a-icon-alt">4 Stars &amp; Up</span>, we can avoid these elements by
            # searching for '&' character in the element.
            if('&' not in str(product)):
                productFoundInPage += 1
                timestamp = datetime.datetime.fromtimestamp(
                    time.time()).strftime('%d-%m-%Y %H:%M:%S %p')
                # There are two types of elements containing the product information.
                # 1st type
                fullProduct = product.parent.parent.parent.parent.parent.parent.parent
                # 2nd type
                classAttr = fullProduct.get('class')
                if(set(['a-section', 'a-spacing-none']) <= set(classAttr)):
                    if(len(classAttr) > 2):
                        fullProduct = product.parent.parent.parent.parent.parent.parent
                # Find product's name.
                # Three ways to find product's name from the two types of product elements mentioned above.
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
                            print("Unable to find the 'product's name' in the product element (", str(
                                fullProduct), ")")
                            exit()
                # Find if product is sponsored or not.
                isSponsored = fullProduct.find(
                    class_="s-label-popover-default")
                if(isSponsored):
                    isSponsored = True
                else:
                    isSponsored = False
                # Find start rating of the product.
                starRating = fullProduct.find(class_='a-icon-alt')
                if(starRating):
                    starRating = starRating.text
                    starRating = starRating.split('out', 1)[0]
                    starRating = starRating.strip()
                else:
                    print("Unable to find 'star rating' in the product element (", str(
                        fullProduct), ")")
                    exit()
                # Find review count of the product.
                # Two ways to find 'number of reviews' in a product element, will use the second one if first fails.
                reviewCount = fullProduct.find(class_='a-color-link')
                if(reviewCount):
                    reviewCount = reviewCount.text
                    reviewCount = reviewCount.replace(',', '')
                    if(reviewCount.isnumeric() == False):
                        print("'Total number of reviews' is a string (the variable might have alphabets or other characters (which are not numbers or alphabets)), \
                                it should be a number(", str(fullProduct), ")")
                        exit()
                else:
                    reviewCount = fullProduct.find(class_='a-size-base')
                    if(reviewCount):
                        reviewCount = reviewCount.text
                        reviewCount = reviewCount.replace(',', '')
                        if(reviewCount.isnumeric() == False):
                            print("'Total number of reviews' is a string (the variable might have alphabets or other characters (which are not numbers or alphabets)), \
                                it should be a number(", str(fullProduct), ")")
                            exit()
                    else:
                        print("Unable to find the 'total number of review' in the product element (", str(
                            fullProduct), ")")
                        exit()

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
        # Introduce random delay between each page requests.
        # Give user the option to send page to the debugger function when the script finds 0 star element in the html.
        # Sometimes amazon.in detects that we are a bot and it drops our requests.
        fileName = timestamp + " - " + url + ".html"
        if(enableDebugMode == False and productFoundInPage == 0):
           print('0 start element found in page')
           # while True:
              #   userChoice = str(input(
              #       "0 star elements found in the page. Do you want to send this page to the debugger? (y/n) "))
              #   if(userChoice == 'y'):
              #       writeEntirePage(fileName, soup, productFoundInPage,
              #                       uniqueProductCount, len(products), url)
              #       break
              #   elif(userChoice == 'n'):
              #       break
              #   else:
              #       print("Invalid input entered. Please enter y or n...")
        if(enableDebugMode == True):
            writeEntirePage(fileName, soup, productFoundInPage,
                            uniqueProductCount, len(products), url)
        print("Found ", productFoundInPage, " products in ", url,
              " out of which ", uniqueProductCount, " are new.")
        # Avoid time delay for last page
        if(args.delay is not None and pageNumber < totPages):
            randomNumber = random.randint(args.delay[0], args.delay[1])
            time.sleep(randomNumber)

productCollection.to_csv('output.csv', index=False)
if(not args.use_settings_from_last_session):
    settingsFiles = open('settings.cfg', 'w')
    settings = {
        '--debugger': args.debugger,
        '--debugger-zero': args.debugger_zero,
        '--delay': args.delay,
        '--keywords': args.keywords,
        '--append': args.append,
        '--page': args.page,
        '--rerun': args.rerun,
        '--batch': args.batch,
        '--verbose': args.verbose
    }
    settings = json.dumps(settings, indent=4, sort_keys=True)
    settingsFiles.write(settings)
    settingsFiles.close()
