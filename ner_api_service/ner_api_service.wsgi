#! /usr/bin/python

import sys
sys.path.insert(0, "/var/www/ner_api")
sys.path.insert(0, "/usr/local/lib/python3.8/site-packages")
sys.path.insert(0, "/usr/local/bin")

import os
os.environ['PYTHONPATH'] = "/usr/local/bin/python"

from api import app as application
