# Myntra scraper

## How to Use

1. Visit [myntra.com](https://www.myntra.com) and search for the item you want to scrape by using its name ('comforter' (a blanket type item) for example).
2. Open the Developer Tools in your browser (usually by right-clicking and selecting "Inspect" or pressing `Ctrl+Shift+I` or `Cmd+Option+I`).
3. Apply any filter to narrow down the search results.
4. Remove all the applied filters.
5. Go to the Network tab.
6. Look for a network request in the Network tab that looks like this `https://www.myntra.com/gateway/v2/search/comforter?rawQuery=comforter&rows=50&o=0&plaEnabled=false&xdEnabled=false&pincode=600004`, 'comforter' is the search key and 'rawQuery=comforter&rows=50&o=0&plaEnabled=false&xdEnabled=false&pincode=600004' is the query params in this case.
7. Open the request and copy the query params and the search key.
8. Replace the query params and the search key from the file key.py

```python
def get_key():
    return 'comforter'

def get_default_params():
    return {
        'f': 'Gender:men,men women',
        'plaEnabled': 'false',
        'xdEnabled': 'false',
        'pincode': '',
    }
```

9. Run the script (myntra.py)...
10. The results will be stored in './data.csv'
