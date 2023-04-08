import requests
import json
import csv

def get_cookies():
    return {
        'bm_sz': '4DE44E7353CD39F169289A2D70A4631B~YAAQXLopF5VqDFqHAQAAUKHoXhN1c94YAGwiv9baO1ZgCjQWe5VVzUGdmhe48t43JS93bXWoB2GvtgH9CGGIZOn7fAWj4bC3MemMvSlbjVRpcGAU2HVnvrQNG6+kxNpLntz4bZ3wQ2lJoJe7PAI+35APttsZ30idfylM3nvVz1YPsuH73Z6oN+FnyvVvMSlZIUXo+VcMMWzqpNjXo47GNOCrSjYp73PmhNFd3yF7JWWN7GH571+FOQstEFzMeAdrTJubhc8eXSNOKz/irbAQzf/dlpsHYvPhJJ96001UgrHOAfc=~4473921~3753524',
        '_d_id': '6e83fb7f-959f-4c1f-b61d-2221347380d9',
        'mynt-eupv': '1',
        'at': 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTnpKbE5qbGhZemt0WkRWaVpDMHhNV1ZrTFdGa09EZ3RPVFkyT0RnNE5EWXpPVGxtSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUyT1RZME56WTFNVGNzSW1semN5STZJa2xFUlVFaWZRLjRLWWtkYy1keTJ2YjJJa1BjYmxMeUhTQ1JvVkRGV3g1Y1lGMS1aODJXZTA=',
        'mynt-ulc-api': 'pincode%3A600005',
        'mynt-loc-src': 'expiry%3A1680929171598%7Csource%3AIP',
        '_abck': 'AA126E0FA961DCDDA0B75EA4412BBFE3~0~YAAQXLopF6MwDVqHAQAATlIlXwlXPqxtoge4V/V1sQZJ3ip9Q2Bbd3q+OzD3cB2qkA2UnhpJvhcVDGivBObypQKx8v5V9xIqWSRpK1m6CfukNT9ldrxa5sfOewex+kkDJkIZlWowkowqMdyjbGBxhpYMIk6eaA+lOVTYlJbqbY5Hdh+5wM7kzbdKWzUQ4ESfb4HMGiFh+gtj60zbjTC1ZBpDTYwggSNRZZCkJa0s9dm1MWBFogiQv1gSfnfIng2Q3hCn58pNvDppzLWF5gp6sN08ugIOuoVdjxn+yR3lyi6Wuk5aOcAPuPVRU6EETj5YkRMylmgD626MM8z4hc4RToDkLHvdY91fDvm1wt1rA6uv/3H+ymJQ6BTKxYo5DPWwe+6Nd2LZC8tGjpE5ZgIGI0VcCN5hSa+n~-1~-1~1680932019',
        'AKA_A2': 'A',
        '_xsrf': 'tw6uie0sXgw2OFWkSpYKSA6MNsLGInSn',
        'utrid': 'ABB4Rk4FZ0ZLWxRVZEFAMCM3Mjk2NDY4NjgkMg%3D%3D.c3cfeb1edf05268a56eecb97c863a14b',
    }

def get_headers(): 
    return {
        'authority': 'www.myntra.com',
        'accept': 'application/json',
        'accept-language': 'en-GB,en;q=0.9',
        'app': 'web',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        # 'cookie': 'bm_sz=4DE44E7353CD39F169289A2D70A4631B~YAAQXLopF5VqDFqHAQAAUKHoXhN1c94YAGwiv9baO1ZgCjQWe5VVzUGdmhe48t43JS93bXWoB2GvtgH9CGGIZOn7fAWj4bC3MemMvSlbjVRpcGAU2HVnvrQNG6+kxNpLntz4bZ3wQ2lJoJe7PAI+35APttsZ30idfylM3nvVz1YPsuH73Z6oN+FnyvVvMSlZIUXo+VcMMWzqpNjXo47GNOCrSjYp73PmhNFd3yF7JWWN7GH571+FOQstEFzMeAdrTJubhc8eXSNOKz/irbAQzf/dlpsHYvPhJJ96001UgrHOAfc=~4473921~3753524; _d_id=6e83fb7f-959f-4c1f-b61d-2221347380d9; mynt-eupv=1; at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTnpKbE5qbGhZemt0WkRWaVpDMHhNV1ZrTFdGa09EZ3RPVFkyT0RnNE5EWXpPVGxtSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUyT1RZME56WTFNVGNzSW1semN5STZJa2xFUlVFaWZRLjRLWWtkYy1keTJ2YjJJa1BjYmxMeUhTQ1JvVkRGV3g1Y1lGMS1aODJXZTA=; mynt-ulc-api=pincode%3A600005; mynt-loc-src=expiry%3A1680929171598%7Csource%3AIP; _abck=AA126E0FA961DCDDA0B75EA4412BBFE3~0~YAAQXLopF6MwDVqHAQAATlIlXwlXPqxtoge4V/V1sQZJ3ip9Q2Bbd3q+OzD3cB2qkA2UnhpJvhcVDGivBObypQKx8v5V9xIqWSRpK1m6CfukNT9ldrxa5sfOewex+kkDJkIZlWowkowqMdyjbGBxhpYMIk6eaA+lOVTYlJbqbY5Hdh+5wM7kzbdKWzUQ4ESfb4HMGiFh+gtj60zbjTC1ZBpDTYwggSNRZZCkJa0s9dm1MWBFogiQv1gSfnfIng2Q3hCn58pNvDppzLWF5gp6sN08ugIOuoVdjxn+yR3lyi6Wuk5aOcAPuPVRU6EETj5YkRMylmgD626MM8z4hc4RToDkLHvdY91fDvm1wt1rA6uv/3H+ymJQ6BTKxYo5DPWwe+6Nd2LZC8tGjpE5ZgIGI0VcCN5hSa+n~-1~-1~1680932019; AKA_A2=A; _xsrf=tw6uie0sXgw2OFWkSpYKSA6MNsLGInSn; utrid=ABB4Rk4FZ0ZLWxRVZEFAMCM3Mjk2NDY4NjgkMg%3D%3D.c3cfeb1edf05268a56eecb97c863a14b',
        'pragma': 'no-cache',
        'referer': 'https://www.myntra.com/t-shirt?f=Brand%3ANUSYL%3A%3AGender%3Aboys%2Cboys%20girls&p=2&rf=Price%3A104.0_803.0_104.0%20TO%20803.0',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-location-context': 'pincode=600005;source=IP',
        'x-meta-app': 'channel=web',
        'x-myntra-app': 'deviceID=6e83fb7f-959f-4c1f-b61d-2221347380d9;customerID=;reqChannel=web;',
        'x-myntraweb': 'Yes',
        'x-requested-with': 'browser',
    }

def get_rows():
    return 50

def get_params(p = 1): 
    return  {
        'f': 'Brand:NUSYL::Gender:boys,boys girls',
        'p': str(p),
        'rf': 'Price:104.0_803.0_104.0 TO 803.0',
        'rows': str(get_rows()),
        'o': '49',
        'plaEnabled': 'false',
        'xdEnabled': 'false',
        'pincode': '',
    }


def get_total_pages():
    response = make_request()
    totalCount = response['totalCount']
    rows = get_rows()
    if(totalCount % rows == 0):
        return int(totalCount / rows) 
    else:
        return int(totalCount / rows) + 1 

def get_key(): 
    return 't-shirt'

def make_request(p = 1):
    cookies = get_cookies()
    headers = get_headers()
    params = get_params()
    key = get_key()
    response = json.loads(requests.get('https://www.myntra.com/gateway/v2/search/' + key, params=params, cookies=cookies, headers=headers).text)
    return response

def get_products(p = 1):
    response = make_request()
    return response['products']

unique_product_ids = set()
unique_products = []
total_pages = get_total_pages()
for i in range(1, total_pages+1):
    products = get_products(i)
    for product in products:
        if product["productId"] not in unique_product_ids:
            unique_product_ids.add(product["productId"])
            unique_products.append(product)

fieldnames = ["productId", "productName", "price", "rating", "ratingCount"]
with open("myntra.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product in unique_products:
        row = {key: product[key] for key in fieldnames}
        writer.writerow(row)

