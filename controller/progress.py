# -*- coding: utf-8 -*-
"""
    playground.controller.progress
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    상태표시 테스트
"""


from flask import render_template, Response, redirect \
                , url_for
from playground.playground_blueprint import playground
import time

@playground.route('/page')
def get_page():
    # return redirect(url_for('.progress'))
    return render_template('progress.html')


@playground.route('/progress')
def progress():
    def generate():
        x = 0
        while x < 110:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)

    return Response(generate(), mimetype= 'text/event-stream')
