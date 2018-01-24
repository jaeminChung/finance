# -*- coding: utf-8 -*-
"""
    playground.blueprint
    ~~~~~~~~~~~~~~~~~~

    playground 어플리케이션에 적용할 blueprint 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import Blueprint
from playground.playground_logger import Log

playground = Blueprint('playground', __name__,
                     template_folder='../templates', static_folder='../static')

Log.info('static folder : %s' % playground.static_folder)
Log.info('template folder : %s' % playground.template_folder)
