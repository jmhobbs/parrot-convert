# -*- coding: utf-8 -*-


class BaseConfig(object):
    ENV = 'PRODUCTION'

    DEBUG = False
    TESTING = False

    TIMEZONE = "UTC"

    # Max POST request size
    MAX_CONTENT_LENGTH = int(1.2 * 1024 * 1024)  # 1MB uploads + breathing room


class TestConfig(BaseConfig):
    ENV = 'TESTING'

    TESTING = True
    CSRF_ENABLED = False
