# -*- coding: utf-8 -*-
"""
    finane.playground_config
    ~~~~~~~~

    playground 디폴트 설정 모듈.
    playground 어플리케이션에서 사용할 디폴트 설정값을 담고 있는 클래스를 정의함.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


class PlaygroundConfig(object):
    #: 데이터베이스 연결 URL
    DB_URL= 'postgresql://pi:skatks123@192.168.0.8:5432'
    #: 데이터베이스 파일 경로
    DB_FILE_PATH= '/finance'
    #: 세션 타임아웃은 초(second) 단위(60분)
    PERMANENT_SESSION_LIFETIME = 60 * 60
    #: 쿠기에 저장되는 세션 쿠키
    SESSION_COOKIE_NAME = 'playground_session'
    #: 로그 레벨 설정
    LOG_LEVEL = 'debug'
    #: 디폴트 로그 파일 경로
    LOG_FILE_PATH = 'resource/log/playground.log'
    #: 디폴트 SQLAlchemy trace log 설정
    DB_LOG_FLAG = 'True'
    


