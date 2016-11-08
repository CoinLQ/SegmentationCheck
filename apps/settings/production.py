from apps.settings.base import *
import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_USERNAME = os.environ.get("SLACK_USERNAME")
