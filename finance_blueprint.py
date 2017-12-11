# -*- coding: utf-8 -*-
"""
    finance.blueprint
    ~~~~~~~~~~~~~~~~~~

    finance 어플리케이션에 적용할 blueprint 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import Blueprint
from finance.finance_logger import Log

finance = Blueprint('finance', __name__,
                     template_folder='../templates', static_folder='../static')

Log.info('static folder : %s' % finance.static_folder)
Log.info('template folder : %s' % finance.template_folder)
