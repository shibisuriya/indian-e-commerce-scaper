from flask import Flask, request
import os
from bs4 import BeautifulSoup
import requests
import random  
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def specific_string(length):  
    sample_string = 'pqrstuvwxyaksdjhkasdlkjqluwoelkansldknc' # define the specific string  
    # define the condition for random string  
    result = ''.join((random.choice(sample_string)) for x in range(length))  
    return result

@app.route('/')
def index():
    return app.send_static_file('./index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape():
    data = request.get_json() 
    key = data['keys'][0]
    pageNumber = 1
    url = 'https://www.amazon.in/s?k=' + key + \
        '&ref=nb_sb_noss_2&page=' + str(pageNumber)
    
    headers = {
        'User-Agent': specific_string(random.randint(1,999)),
        'From': specific_string(random.randint(1,999)) 
    }

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html5lib')
    items = soup.select('.a-icon-star, .a-icon-star-small')
    elements = [] 
    for star in items:
        product = star.parent.parent.parent.parent.parent.parent # Wrote this using 'trail and error' method.
        produce_name = product.select('.a-size-base-plus')[0]
        #produce_name = ''
        product_obj = {
            "name": str(produce_name),
            "html": str(product)
        }
        print(product_obj)
        elements.append(product_obj)
    return elements
    # return page.content 
    # soup = BeautifulSoup(page.content, 'html5lib')




if __name__ == '__main__':
    # serve static files from the "static" directory
    app.static_folder = 'static'
    app.run(debug=True,  host='0.0.0.0', port=4000)