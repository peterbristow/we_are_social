from base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Stripe environment variables
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_gxQDf9QL5eKhTgDpoWr560AP')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_WODOSCNhYTVcDu7nHCnnp34A')

# Paypal environment variables
SITE_URL = 'http://<your Heroku app name>.herokuapp.com'
PAYPAL_NOTIFY_URL = '<your Heroku URL>'
PAYPAL_RECEIVER_EMAIL = 'peterjb73+1@gmail.com'
