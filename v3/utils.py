from key import key
import requests
import random  
from bs4 import BeautifulSoup


def get_key(title, image):
    return f"{title}-{image}"

def specific_string(length):  
    sample_string = 'pqrstuvwxyaksdjhkasdlkjqluwoelkansldknc' # define the specific string  
    # define the condition for random string  
    result = ''.join((random.choice(sample_string)) for x in range(length))  
    return result

cookies = {
    'session-id': '261-1163646-2292460',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'INR',
    'ubid-acbin': '262-5280853-8370053',
    'session-token': '0Yx/sl7jsWUnMhSpZuNhnhoitPCy/P87wflbutp1yQrh8Yb7bcu/iy3Pq6+mwfvbHPt5levtC+EpVnMKlrXlieqJfd4SHBcO9/fKvQVmGwljmQpqwB64900L33gAXKg3/CY2GA19uLkuW5syRtu0GcyU6SvUfupuV4+E0Rd4U5kuWuzVWlNYH/uGVOJA2vhioSLTEh56fG2jrmtzmwZXX9qsZVVQjGaaqT729Q99uP8=',
    'csm-hit': 'tb:s-RCA08544A2YQCT2J63XM|1684211284757&t:1684211285532&adb:adblk_no',
}

headers = {
            'User-Agent': specific_string(random.randint(1,999)),
            'From': specific_string(random.randint(1,999)) 
}

params = {
    'k': key,
}


def is_last_page(page):
    next_button = page.find('a', class_="s-pagination-next")
    if(next_button):
        classes_list = next_button['class']
        return bool('s-pagination-disabled' in classes_list)
    else:
        return True
    


def get_soup(page_number): 
    params['page'] = str(page_number)
    response = requests.get('https://www.amazon.in/s', params=params, cookies=cookies, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')

def get_star_elements(soup):
    return soup.find_all(class_='a-icon-star-small')
