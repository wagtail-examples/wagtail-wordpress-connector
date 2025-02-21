from .base import *  # noqa F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-hyz%gvhpby_ghqqsk=9t2c+s6*!5xez7@29xf&e(!)oe=^5^(7"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Remove if not required
INSTALLED_APPS += ["style_guide", "django_extensions"]  # noqa F405

# To stop the redirects from being created when a page is moved
# Use the redirects action in the import action to create the redirects
# It's likely you would want to set this to True in production
# e.g. when you are no longer using the import actions
WAGTAILREDIRECTS_AUTO_CREATE = False

# Comment out if you need to use timezone aware datetimes
USE_TZ = False

# Shell plus config
SHELL_PLUS_IMPORTS = [
    "from wp_connector.client import *",
    "from wp_connector.exporter import *",
    "from wp_connector.field_panels import *",
    "from wp_connector.importer import *",
    "from wp_connector.richtext_field_processor import *",
    "from wp_connector.streamfieldable import *",
]

try:
    from .local import *  # noqa F403
except ImportError:
    pass
