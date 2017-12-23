# -*- coding: utf-8 -*-
"""
    finance.controller.daum_cartoon
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    다음 만화 내려받기
"""


from flask import render_template, request, current_app, session, redirect \
                 , url_for, Response
from functools import wraps
from werkzeug import check_password_hash
from wtforms import Form, TextField, PasswordField, HiddenField, validators

from finance.database import dao
from finance.finance_logger import Log
from finance.finance_blueprint import finance
import urllib.request, re, os, json
from os import path


def saveToon(filename, imgURL):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
       'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
       'Accept-Encoding': 'gzip, deflate',
       'Accept-Language': 'en-US,en;q=0.5',
       'Referer': 'http://webtoon.daum.net/#day=wed&tab=day',
       'Connection': 'keep-alive'}

    req = urllib.request(imgURL, headers=hdr)

    try:
        img = urllib.request.urlopen(req)
    except(urllib.request.HTTPError, e):
        Log.error(e.fp.read())

    file = open(filename, 'wb')
    file.write(img.read())
    file.close()

@finance.route('/daum_cartoon')
def daum_cartoon_form():
    """다음 만화 목록 표시해야하지만,
       일단 만화 아이디 받아서 내려받기"""
    title_id = request.args.get('title_id', '')
    form = DaumCartoonForm(request.form)
    
    return render_template('daum_cartoon.html',
                           form=form,
                           title_id=title_id)


@finance.route('/daum_cartoon', methods=['POST'])
def daum_cartoon():
    form = DaumCartoonForm(request.form)
    title_id = form.title_id.data
    if form.validate():
        session.permanent = True

    # collectCartoonList(base_url, title_id)
        
    return redirect(url_for('.daum_cartoon_download',
                           title_id=title_id))


@finance.route('/daum_cartoon_download/<title_id>')
def daum_cartoon_download(title_id) :
    url = 'http://webtoon.daum.net/data/pc/webtoon/'
    if not os.access(title_id, os.F_OK):
        os.makedirs(title_id)
        
    listhtml = urllib.request.urlopen('%sview/%s?timeStamp=' % (url, title_id)).read()
    listjson = json.loads(listhtml)
    ids = []
    for episode in listjson['data']['webtoon']['webtoonEpisodes']:
        ids.append(episode['id'])
    ids.sort()
    total = len(ids)
    Log.info('Total episode count : %s' % total)

    def generate(ids, title_id, total, url):
        x = 0
        for no, epid in enumerate(ids):
            ephtml = urllib.request.urlopen('%s/viewer_images/%s' % (url, epid)).read()
            epjson = json.loads(ephtml)
            for epimage in epjson['data']:
                fileName = '%s/%s%s.png' % \
                           (title_id, str(no+1).zfill(4), str(epimage['imageOrder']).zfill(2))
                saveToon(fileName, epimage['url'])
                Log.info('Episode %s/%s saved' % (no+1, total))
                yield "data:" + str(x) + "\n\n"
                x = (no+1) / total * 100

    return Reponse(generate(ids, title_id, total, url), mimetype='text/event-stream')
    
        
class DaumCartoonForm(Form):
    title_id = TextField('Title id',
                         [validators.Required('ID를 입력하세요.')])
