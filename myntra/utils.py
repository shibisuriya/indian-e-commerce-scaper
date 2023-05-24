from key import get_key, get_default_params
import requests
import json
from headers import get_cookies, get_headers

def get_hash_key(id, name):
    return f"{id}_{name}"

def get_rows():
    return 50

def get_params(p = 1): 
    o = '0'
    rows = get_rows()
    if(p == 1): 
        o = '0'
    else:
        o = str((p - 1 ) * rows - 1)
    
    params = get_default_params()
    params['p'] = str(p)
    params['o'] =  o   
    params['rows'] =  str(rows)
    if(p == 1):
        del params['p']
    return params

def get_total_pages():
    response = make_request()
    totalCount = response['totalCount']
    rows = get_rows()
    if(totalCount % rows == 0):
        return int(totalCount / rows) 
    else:
        return int(totalCount / rows) + 1 

def make_request(p = 1):
    cookies = get_cookies()
    headers = get_headers()
    params = get_params(p)
    key = get_key()
    print('Querying using key -> ', key, ' and  params -> ', params)
    response = json.loads(requests.get('https://www.myntra.com/gateway/v2/search/' + key, params=params, cookies=cookies, headers=headers).text)
    return response

def get_products(p = 1):
    response = make_request(p)
    return response['products']