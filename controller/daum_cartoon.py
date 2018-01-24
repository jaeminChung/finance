# -*- coding: utf-8 -*-
"""
    playground.controller.daum_cartoon
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    다음 만화 내려받기
"""


from flask import render_template, request, current_app, session, redirect \
                 , url_for, Response
from functools import wraps
from werkzeug import check_password_hash
from wtforms import Form, TextField, PasswordField, HiddenField, validators

from playground.database import dao
from playground.playground_logger import Log
from playground.playground_blueprint import playground
import urllib.request, re, os, json
from os import path

url = 'http://webtoon.daum.net/data/pc/webtoon/'

def saveToon(filename, imgURL):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
       'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
       'Accept-Encoding': 'gzip, deflate',
       'Accept-Language': 'en-US,en;q=0.5',
       'Referer': 'http://webtoon.daum.net/#day=wed&tab=day',
       'Connection': 'keep-alive'}

    req = urllib.request.Request(imgURL, headers=hdr)

    try:
        img = urllib.request.urlopen(req)
    except(urllib.request.HTTPError, e):
        Log.error(e.fp.read())

    file = open(filename, 'wb')
    file.write(img.read())
    file.close()


def get_daum_cartoon_id_list(title_id):
    if not os.access(title_id, os.F_OK):
        os.makedirs(title_id)

    resource = urllib.request.urlopen('%sview/%s?timeStamp=' % (url, title_id))
    listhtml = resource.read().decode('UTF-8')
    listjson = json.loads(listhtml)
    ids = []
    for episode in listjson['data']['webtoon']['webtoonEpisodes']:
        ids.append(episode['id'])
    ids.sort()

    return ids

    
@playground.route('/daum_cartoon')
def daum_cartoon_form():
    """다음 만화 목록 표시해야하지만,
       일단 만화 아이디 받아서 내려받기"""
    
    return render_template('daum_cartoon.html')


@playground.route('/daum_cartoon', methods=['POST'])
def daum_cartoon():
    title_id = request.form['title_id']
    total = len(get_daum_cartoon_id_list(title_id))

    Log.info('다음만화 다운로드 : ' + title_id)
        
    return render_template('daum_cartoon_download.html',
                           title_id=title_id,
                           total=total)


@playground.route('/daum_cartoon_download/<title_id>/<total>')
def daum_cartoon_download(title_id, total) :
    ids = get_daum_cartoon_id_list(title_id)

    
    def generate(ids, title_id, total):
        for no, epid in enumerate(ids):
            resource = urllib.request.urlopen('%s/viewer_images/%s' % (url, epid)).read()
            ephtml = resource.decode('UTF-8')
            epjson = json.loads(ephtml)
            if epjson['data'] :
                for epimage in epjson['data']:
                    fileName = '%s/%s%s.png' % \
                               (title_id, str(no+1).zfill(4), str(epimage['imageOrder']).zfill(2))
                    saveToon(fileName, epimage['url'])
            yield "data:" + str(no+1) + "\n\n"

            
    return Response(generate(ids, title_id, total), mimetype='text/event-stream')
