from config.components.apps import INSTALLED_APPS
from config.components.restful import REST_FRAMEWORK


DEVELOPING_APPS = [
    'django_extensions',
]

INSTALLED_APPS.extend(DEVELOPING_APPS)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
    'rest_framework.renderers.BrowsableAPIRenderer',
)
