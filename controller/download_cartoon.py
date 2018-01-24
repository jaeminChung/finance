# -*- coding: utf-8 -*-
"""
    playground.controller.download_cartoon
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    내려받은 만화 압축해서 다운로드 링크 보여주기
"""


from flask import render_template, request, redirect, url_for
from functools import wraps
from wtforms import Form, TextField, PasswordField, HiddenField, validators

from playground.playground_logger import Log
from playground.playground_blueprint import playground
import zipfile, shutil
from zipfile import ZipFile


@playground.route('/zip_cartoon/<title_id>')
def zip_cartoon(title_id):
    """다운로드 받은 만화 폴더 압축하고 해당 폴더는 지우기"""
# def dir2zip(dir, zipName, silent, delete):
# dir2zip(basedir, basedir+'.zip', 'nosilent', 'delete')
    zip = ZipFile(zipName, "w", zipfile.ZIP_DEFLATED)
    for file in getFileListInDir(dir):
        zip.write(path.relpath(file))
        if not silent:
            print "Add:", file
    zip.close()
    shutil.rmtree(dir)

    return render_template('save_cartoon.html')

@playground.route('/save_cartoon/<title_id>')
def save_cartoon(title_id):
