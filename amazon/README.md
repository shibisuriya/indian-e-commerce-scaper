# amazon.in scraper

Scrape products from Amazon.in and export them to a CSV.

## How to run?

If you want to scrape all the shirts listed in amazon.in, then open `./src/key.py` and
and set 'shirt' as value for the python variable 'key'.

in `./src/key.py`,

```py
key = 'shirt'
```

And run,

`docker-compose up`
