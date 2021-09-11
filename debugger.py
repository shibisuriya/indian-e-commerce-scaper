import os
import sys

def writeEntirePage(fileName, soup, productFoundInPage, uniqueProductCount, totalStarElementFoundInpage, url):
    # Write entire page
    # Clear debugger file
    if not os.path.isdir("DebuggerOutput"):
        print("DebuggerOutput directory doesn't exist... Creating DebuggerOutput directory...")
        try: 
            os.makedir("DebuggerOutput")
        except:
            sys.exit("Unable to create DebuggerOutput directory...")
            
    entirePageFile = open( "./DebuggerOutput/" + fileName, "w")
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
    entirePageFile.close()

    # Note down the page information in a .csv file.


