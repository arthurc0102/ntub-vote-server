from config.settings import root, env


# Build paths inside the project like this: root(...)
BASE_DIR = root()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGINS', default=[])

SHOW_DOCS = env('SHOW_DOCS', default=False)

VOTE_ADMIN = env('VOTE_ADMIN', default=False)
