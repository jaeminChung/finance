# -*- coding: utf-8 -*-
"""
    finance.controller.scraping_daum_stock
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    종목정보 조회, 주가 정보 저장
"""

from flask import render_template, request

import re
import urllib.parse
import urllib.request

import pandas as pd
from sqlalchemy import create_engine
from finance.database import dao
from finance.model.stock import Stock
from finance.model.stock_price import StockPrice
from finance.finance_blueprint import finance
from finance.finance_logger import Log

def download_stock_codes(market=None, delisted=False):
    """MARKET_CODE_DICT 중 하나의 종목코드 정보 전체를 DataFrame으로 가져온다."""
    DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'

    MARKET_CODE_DICT = {
        'kospi': 'stockMkt',
        'kosdaq': 'kosdaqMkt',
        'konex': 'konexMkt'
    }
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


def save_stock_codes():
    """코스피 전체 종목 정보를 '종목' 테이블에 저장한다."""
    engine = get_postgres_engine()
    kospi_stocks = download_stock_codes('kospi')
    kospi_stocks.to_sql('종목', engine, if_exists='append')


def visit_page(url):
    """url을 방문하여 html을 UTF-8로 인코딩하여 리턴한다."""
    try:
        page = urllib.request.urlopen(url)
    except urllib.request.HTTPError as e:
        print(e.fp.read())

    return str(page.read().decode('UTF-8'))


def extract_stock_info(html):
    """다음 일일주가정보 페이지에서 주가정보 부분만 추출한다."""
    pattern = r'(?ims)<td class="datetime2">(\d{2}\.\d{2}.\d{2})</td>\s+'
    pattern = pattern + r'((<td class="num">[\d,]+</td>\s*){4})'
    pattern = pattern + r'.*?(<td class="num">[\d,]+</td>)'
    stock_info = re.findall(pattern, html)
    return stock_info


def extract_daily_info(info):
    """extract_stock_info에서 추출된 주가정보중 일자별 주가정보를 추출한다."""
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
    return daily_info

    
def get_next_page(html, page):
    """다음 페이지 번호를 추출한다."""
    pattern = r'(?im)<span class="on">.+?</span>.+?javascript:goPage\(\'(\d+)\''
    next_page = re.findall(pattern, html)
    if len(next_page) > 0:
        return int(next_page[0])
    else:
        return 0


def save_stock_price(stock_code, page=1):
    """특정 페이지의 일자별 주가정보를 모두 추출하여 테이블에 저장한다."""
    STOCK_INFO_URL = \
        'http://finance.daum.net/item/quote_yyyymmdd_sub.daum?modify=1=&code={code}&page='
    url=STOCK_INFO_URL.replace('{code}', stock_code)
    
    page_html = visit_page(url+str(page))
    stock_info = extract_stock_info(page_html)
    for info in stock_info:
        daily_info = extract_daily_info(info)
        try:
            exist = dao.query(StockPrice). \
                    filter_by(종목코드=stock_code,거래일자=daily_info['날짜']). \
                    first()
            if not exist:
                stock_price = StockPrice(stock_code,
                                         daily_info['날짜'],
                                         daily_info['시가'].replace(',',''),
                                         daily_info['고가'].replace(',',''),
                                         daily_info['저가'].replace(',',''),
                                         daily_info['종가'].replace(',',''),
                                         daily_info['거래량'].replace(',',''))
                dao.add(stock_price)
                dao.commit()
        except Exception as e:
            error = "DB에러발생 : " + str(e)
            Log.error(error)
            dao.rollback()
            raise e
        

    next_page = get_next_page(page_html, page)

    if next_page > 0:
        return save_stock_price(stock_code, next_page)    
    else:
        return render_template('save_stock_info.html',
                               stock_code=stock_code)


def get_postgres_engine():
    """SQLAlchemy engine 객체를 리턴한다."""
    _engine = create_engine('postgresql://pi:skatks123@localhost:5432/finance', echo=True)
    return _engine


@finance.route('/show_stock_list')
def show_stock_list():
    stock_list = dao.query(Stock).order_by(Stock.company_name.asc()).all()
    
    return render_template('show_stock_list.html',
                           stocks=stock_list)


@finance.route('/save_stock_info/<stock_code>')
def save_stock_info(stock_code):
    #종목코드 조회
    #종목코드별 일일주가정보저장
    if stock_code:
        return save_stock_price(stock_code)
    else:
        return render_template('save_stock_info.html')

