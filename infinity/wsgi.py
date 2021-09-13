import os

import dotenv


dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infinity.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Settings')

from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()
