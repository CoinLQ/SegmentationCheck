# -*- coding: utf-8 -*-

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import os
from django.conf import settings
import six
import logging

def get_qiniu_config(name, default=None):
    """
    Get configuration variable from environment variable
    or django setting.py
    """
    config = os.environ.get(name, getattr(settings, name, default))
    if config is not None:
        if isinstance(config, six.string_types):
            return config.strip()
        else:
            return config
    else:
        raise ImproperlyConfigured(
            "Can't find config for '%s' either in environment"
            "variable or in setting.py" % name)


QINIU_ACCESS_KEY = get_qiniu_config('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = get_qiniu_config('QINIU_SECRET_KEY')
QINIU_BUCKET_NAME = get_qiniu_config('QINIU_BUCKET_NAME')


def init_qiniu():
	#需要填写你的 Access Key 和 Secret Key
	access_key = QINIU_ACCESS_KEY
	secret_key = QINIU_SECRET_KEY

	#构建鉴权对象
	q = Auth(access_key, secret_key)

	return q

def upload_file(file_name, key, prefix=''):
	resource_key = prefix+key
	q =  init_qiniu()
	token = q.upload_token(QINIU_BUCKET_NAME, resource_key, 3600)
	ret, info = put_file(token, resource_key, file_name)
	if not ret:
		logger = logging.getLogger(__name__)
		logger.error(info)
	return ret