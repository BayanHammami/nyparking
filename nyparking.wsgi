#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/nyparking/app")
sys.path.insert(1,"/var/www/nyparking")

from app import app as application