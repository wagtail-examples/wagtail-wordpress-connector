from .base import *  # noqa F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-hyz%gvhpby_ghqqsk=9t2c+s6*!5xez7@29xf&e(!)oe=^5^(7"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Remove if not required
INSTALLED_APPS += ["style_guide"]  # noqa F405

try:
    from .local import *  # noqa F403
except ImportError:
    pass
