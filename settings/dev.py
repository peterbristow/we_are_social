"""
Provides the settings used for the development environment:
What will happen here is that we'll tell Django which environment to use whenever we run any of our manage.py commands.
    E.g. python manage.py runserver --settings=settings.dev
"""
from base import *

DEBUG = True

INSTALLED_APPS.append('debug_toolbar')

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
SITE_URL = 'http://127.0.0.1:8000'
PAYPAL_NOTIFY_URL = '<your heroku URL>'
PAYPAL_RECEIVER_EMAIL = 'peterjb73+1@gmail.com'
