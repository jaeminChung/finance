# -*- coding: utf-8 -*-
"""
    finance.controller.progress
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    상태표시 테스트
"""


from flask import render_template, request, current_app, session, redirect \
                 , url_for
from functools import wraps
from werkzeug import check_password_hash
from wtforms import Form, TextField, PasswordField, HiddenField,


@app.route('/page')
def get_page():
    return send_file('templates/progress.html')


@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x < 100:
            print x
            x = x + 10
            time.sleep(0.2)
            yield "data:" + str(x) + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')
