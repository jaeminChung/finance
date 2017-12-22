# -*- coding: utf-8 -*-
"""
    finance.controller.progress
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    상태표시 테스트
"""


from flask import render_template, Response, redirect \
                , url_for
from finance.finance_blueprint import finance
import time

@finance.route('/page')
def get_page():
    # return redirect(url_for('.progress'))
    return render_template('progress.html')


@finance.route('/progress')
def progress():
    def generate():
        x = 0
        while x < 110:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)

    return Response(generate(), mimetype= 'text/event-stream')
