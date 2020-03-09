from .base import *


def hasallattr(obj, *attrs):
    return all(hasattr(obj, a) for a in attrs)


ALLOWED_HOSTS = [os.getenv("DJANGO_HOST", "127.0.0.1")]

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

insert_idx = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware")
MIDDLEWARE.insert(insert_idx + 1, "whitenoise.middleware.WhiteNoiseMiddleware")

if hasallattr(os.environ, "EMAIL_HOST", "EMAIL_PORT", "EMAIL_USER", "EMAIL_PASSWORD"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_HOST_USER = os.getenv("EMAIL_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False)
    EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", False)
    EMAIL_TIMEOUT = os.getenv("EMAIL_TIMEOUT")

    EMAIL_SSL_KEYFILE = os.getenv("EMAIL_SSL_KEYFILE")
    EMAIL_SSL_CERTIFICATE = os.getenv("EMAIL_SSL_CERTIFICATE")
