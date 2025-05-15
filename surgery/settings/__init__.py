import os

from dotenv import load_dotenv

load_dotenv()
env = os.getenv('DJANGO_ENV', 'dev')

if env == 'prod':
    # DJANGO_ENV=prod python manage.py runserver
    from .prod import *
else:
    from .dev import *
