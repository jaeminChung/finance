# -*- coding: utf-8 -*-
"""
    finance.model.stock_price
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    일별주가정보를 담기 위한 model.
"""


from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime

from finance.model.stock import Stock

from finance.model import Base


class StockPrice(Base):
    __tablename__ = '일별주가'
    
    stock_cd = Column(String(10), ForeignKey(Stock.stock_cd), primary_key=True)
    trading_date = Column(DateTime, primary_key=True)
    start_price = Column(Integer, unique=False)
    max_price = Column(Integer, unique=False)
    min_price = Column(Integer, unique=False)
    end_price = Column(Integer, unique=False)
    trading_amount = Column(Integer, unique=False)


    def __init__(self, stock_cd, trading_date,
                 start_price, max_price, min_price, end_price, trading_amount):
        """일별주가 모델 클래스를 초기화 한다."""
        
        self.stock_cd = stock_cd
        self.trading_date = trading_date
        self.start_price = start_price
        self.max_price = max_price
        self.min_price = min_price
        self.end_price = end_price
        self.trading_date = trading_date

    def __repr__(self):
        """모델의 주요 정보를 출력한다."""        
        
        return '<일별주가 %r %r %r>' % (self.stock_cd, self.trading_date, self.end_price)
