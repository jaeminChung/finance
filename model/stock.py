# -*- coding: utf-8 -*-
"""
    playground.model.stock
    ~~~~~~~~~~~~~~~~~~~

    kospi 종목 정보를 담을 model.
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from playground.model import Base


class Stock(Base):
    __tablename__ = '종목'

    index = Column('index',Integer, unique=True)
    stock_cd = Column('종목코드',String(10), primary_key=True)
    company_name = Column('회사명',String(100), unique=False)
    type_of_biz = Column('업종',String(2000), unique=False)
    product = Column('주요제품',String(2000), unique=False)
    listed_date = Column('상장일',String(10), unique=False)
    closing_account_date = Column('결산월',String(10), unique=False)
    president_name = Column('대표자명',String(1000), unique=False)
    homepage = Column('홈페이지',String(1000), unique=False)
    address = Column('지역',String(1000), unique=False)

    stock_prices = relationship('StockPrice', 
                          backref='stock', 
                          cascade='all, delete, delete-orphan')
    

    def __init__(self, index, stock_cd, company_name
                 , type_of_biz, product, listed_date
                 , closing_account_date, president_name, homepage, address):
        self.index = index
        self.stock_cd = stock_cd
        self.company_name = company_name
        self.type_of_biz = type_of_biz
        self.product = product
        self.listed_date = listed_date
        self.closing_account_date = closing_account_date
        self.president_name = president_name
        self.homepage = homepage
        self.address = address

    def __repr__(self):
        return '<종목 %r %r>' % (self.stock_cd, self.company_name)
    
    
