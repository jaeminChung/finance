import urllib.request
import re


def visit_page(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
       'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
       'Accept-Encoding': 'gzip, deflate',
       'Accept-Language': 'en-US,en;q=0.5',
       'Referer': 'http://finance.daum.net/',
       'Connection': 'keep-alive'}

    req = urllib.request.Request(url) #, headers=hdr)

    try:
        page = urllib.request.urlopen(url)
    except urllib.request.HTTPError as e:
        print(e.fp.read())

    return str(page.read().decode('UTF-8'))


def extract_stock_info(html):
    exp = re.compile(r'(?im)<td class="datetime2">(\d{2}\.\d{2}.\d{2})</td>\s*((<td class="num">[\d,]+</td>\s*){3}).+(<td class="num">[\d,]+</td>)')
    stock_info = exp.findall(html)
    return stock_info


def save_stock_info(url, page):
    page = visit_page(url+str(page))
    stock_info = extract_stock_info(page)
    print(stock_info)
    print('\n')
    # insert_stock_info(stock_info)


# need to be edited
stock_cd = '005930'

base_url = 'http://finance.daum.net/item/quote_yyyymmdd_sub.daum?code=005930&modify=1=&page='

save_stock_info(base_url, 1)

