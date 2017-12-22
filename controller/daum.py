# -*- coding: utf-8 -*-
"""
    finance.controller.daum
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    다음 만화 내려받기
"""


from flask import render_template, request, current_app, session, redirect \
                 , url_for
from functools import wraps
from werkzeug import check_password_hash
from wtforms import Form, TextField, PasswordField, HiddenField, validators

from finance.database import dao
from finance.finance_logger import Log
from finance.finance_blueprint import finance
import urllib2, re, os, json
from os import path

def saveToon(filename, imgURL):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
       'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
       'Accept-Encoding': 'gzip, deflate',
       'Accept-Language': 'en-US,en;q=0.5',
       'Referer': 'http://webtoon.daum.net/#day=wed&tab=day',
       'Connection': 'keep-alive'}

    req = urllib2.Request(imgURL, headers=hdr)

    try:
        img = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()

    file = open(filename, 'wb')
    file.write(img.read())
    file.close()

def collectCartoonList(url, title) :
    if not os.access(title, os.F_OK):
        os.makedirs(title)
        
    listhtml = urllib2.urlopen('%sview/%s?timeStamp=' % (url, title)).read()
    listjson = json.loads(listhtml)
    ids = []
    for episode in listjson['data']['webtoon']['webtoonEpisodes']:
        ids.append(episode['id'])
    ids.sort()
    total = len(ids)
    print('Total episode count : %s' % total)
    
    for no, epid in enumerate(ids):
        ephtml = urllib2.urlopen('%s/viewer_images/%s' % (url, epid)).read()
        epjson = json.loads(ephtml)
        for epimage in epjson['data']:
            fileName = '%s/%s%s.png' % (title, str(no+1).zfill(4), str(epimage['imageOrder']).zfill(2))
            saveToon(fileName, epimage['url'])
        print('Episode %s/%s saved' % (no+1, total))
"""        
# need to be edited
titleId = 'game'
baseurl = 'http://webtoon.daum.net/data/pc/webtoon/'
collectCartoonList(baseurl, titleId)
"""

@finance.route('/daum')
def daum():
    """다음 만화 목록 표시해야하지만,
       일단 만화 아이디 받아서 내려받기"""
    title_id = request.args.get('title_id', '')
    form = DaumCartoonForm(request.form)
    
    return render_template('daum.html',
                           form=form,
                           title_id=title_id)

@finance.route('/daum', methods=['POST'])
def download_cartoon():
    if form.validate():
        session.permanent = True

        title_id = form.title_id.data
        base_url = 'http://webtoon.daum.net/data/pc/webtoon/'
        collectCartoonList(base_url, title_id)
        


class DaumCartoonForm(Form):
    """내려받을 다음만화 아이디를 입력받음"""
    title_id = \
               TextField('Title Id',
                         [validators.Required('만화ID를 입력하세요.')])
