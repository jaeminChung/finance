# -*- coding: utf-8 -*-
"""
    finance.model.stock_price
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    일별주가정보를 담기 위한 model.
"""


from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime

from finance.model.stock import Stock

from finance.model import Base


'''    
    stock_cd = Column(String(10), ForeignKey(Stock.stock_cd), primary_key=True)
    trading_date = Column(DateTime, primary_key=True)
    start_price = Column(Integer, unique=False)
    max_price = Column(Integer, unique=False)
    min_price = Column(Integer, unique=False)
    end_price = Column(Integer, unique=False)
    trading_amount = Column(Integer, unique=False)
'''
class StockPrice(Base):
    __tablename__ = '일별주가'
    종목코드 = Column(String(10), ForeignKey(Stock.stock_cd), primary_key=True)
    거래일자 = Column(DateTime, primary_key=True)
    시가 = Column(Integer, unique=False)
    고가 = Column(Integer, unique=False)
    저가 = Column(Integer, unique=False)
    종가 = Column(Integer, unique=False)
    거래량 = Column(Integer, unique=False)

    def __init__(self, stock_cd, trading_date,
                 start_price, max_price, min_price, end_price, trading_amount):
        """일별주가 모델 클래스를 초기화 한다."""
        
        self.종목코드 = stock_cd
        self.거래일자 = trading_date
        self.시가 = start_price
        self.고가 = max_price
        self.저가 = min_price
        self.종가 = end_price
        self.거래량 = trading_amount

    def __repr__(self):
        """모델의 주요 정보를 출력한다."""        
        
        return '<일별주가 %r %r %r>' % (self.종목코드, self.거래일자, self.종가)
