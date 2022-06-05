import os

import dotenv
from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp


dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infinity.settings.essentials")
os.environ.setdefault("DJANGO_CONFIGURATION", "Settings")


# To read Celery Mixins via class based settings
import configurations

configurations.setup()


app = TenantAwareCeleryApp("infinty")
# app.conf.enable_utc=False
# app.conf.update(timezone='Asia/Kolkata')

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
