# -*- coding: utf-8 -*-
"""
    finance.controller.index
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    빈 화면
"""


from flask import render_template, request, current_app, session, redirect \
                 , url_for
from functools import wraps
from werkzeug import check_password_hash
from wtforms import Form, TextField, PasswordField, HiddenField, validators

from finance.database import dao
from finance.finance_logger import Log
from finance.finance_blueprint import finance


@finance.teardown_request
def close_db_session(exception=None):
    """요청이 완료된 후에 db연결에 사용된 세션을 종료함"""
    
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))


@finance.route('/')
def index():
    """로그인이 성공한 다음에 보여줄 초기 페이지"""
    return render_template('index.html')
