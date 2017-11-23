import urllib.request
import re
import urllib.parse
import pandas as pd

MARKET_CODE_DICT = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt',
    'konex': 'konexMkt'
}

DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'


def download_stock_codes(market=None, delisted=False):
    params = {'method': 'download'}

    if market.lower() in MARKET_CODE_DICT:
        params['marketType'] = MARKET_CODE_DICT[market]

    if not delisted:
        params['searchType'] = 13

    params_string = urllib.parse.urlencode(params)
    request_url = urllib.parse.urlunsplit(['http', DOWNLOAD_URL, '', params_string, ''])

    df = pd.read_html(request_url, header=0)[0]
    df.종목코드 = df.종목코드.map('{:06d}'.format)

    return df


def visit_page(url):
    try:
        page = urllib.request.urlopen(url)
    except urllib.request.HTTPError as e:
        print(e.fp.read())

    return str(page.read().decode('UTF-8'))


def extract_stock_info(html):
    pattern = r'(?ims)<td class="datetime2">(\d{2}\.\d{2}.\d{2})</td>\s+'
    pattern = pattern + r'((<td class="num">[\d,]+</td>\s*){4})'
    pattern = pattern + r'.*?(<td class="num">[\d,]+</td>)'
    stock_info = re.findall(pattern, html)
    return stock_info


def extract_daily_info(info):
    daily_info = {}
    daily_info['날짜'] = info[0]
    
    stock_price_pattern = r'([\d,]+)'
    stock_price = re.findall(stock_price_pattern, info[1])
    
    daily_info['시가'] = stock_price[0]
    daily_info['고가'] = stock_price[1]
    daily_info['저가'] = stock_price[2]
    daily_info['종가'] = stock_price[3]

    tran_volumn = re.findall(stock_price_pattern, info[3])

    daily_info['거래량'] = tran_volumn[0]

#    print(daily_info)
    
def get_next_page(html, page):
    pattern = r'(?im)<span class="on">.+?</span>.+?javascript:goPage\(\'(\d+)\''
    next_page = re.findall(pattern, html)
    if len(next_page) > 0:
        return int(next_page[0])
    else:
        return 0


def save_stock_info(url, page):
    page_html = visit_page(url+str(page))
    stock_info = extract_stock_info(page_html)
    for info in stock_info:
        daily_info = extract_daily_info(info)
    # insert_stock_info(stock_info)

    next_page = get_next_page(page_html, page)
    print(next_page)
    if next_page > 0:
        save_stock_info(url, next_page)


# need to be edited
stock_cd = '005930'

base_url = 'http://finance.daum.net/item/quote_yyyymmdd_sub.daum?code=005930&modify=1=&page='

#save_stock_info(base_url, 1)

kospi_stocks = download_stock_codes('kospi')
print(kospi_stocks.head())

