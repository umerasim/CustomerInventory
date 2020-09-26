#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/apps/CustomerInventory')
from CustomerInventory import app as application
application.secret_key = 'thisIsMySecretKey'