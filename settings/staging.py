import os

from base import *
import dj_database_url

DEBUG = True

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('CLEARDB_DATABASE_URL'))
}

# Stripe environment variables
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_gxQDf9QL5eKhTgDpoWr560AP')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_WODOSCNhYTVcDu7nHCnnp34A')

# Paypal environment variables
SITE_URL = 'http://<your Heroku app name>.herokuapp.com'
PAYPAL_NOTIFY_URL = '<your Heroku URL>'
PAYPAL_RECEIVER_EMAIL = 'peterjb73+1@gmail.com'
