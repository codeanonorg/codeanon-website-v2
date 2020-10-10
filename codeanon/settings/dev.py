from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "74e68$z11#q+ur7=k(z-)%@9-k!=vb9ii@uo3kgfag#4n16oad"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

if "AIRBRAKE_PROJECT_KEY" in os.environ:
    AIRBRAKE["environment"] = "development"

try:
    from .local import *
except ImportError:
    pass
