# -*- coding: utf-8 -*-
"""
    finance.model
    ~~~~~~~~~~~~~~

    finance 어플리케이션에 적용될 model에 대한 패키지 초기화.
"""


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

__all__ = ['stock', 'stock_price']
