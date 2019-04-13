import re
import requests

from config.components.api import NTUB_API_URL, NTUB_API_HEADERS

from rest_framework.exceptions import AuthenticationFailed


INFO_KEYS = ['std_no', 'std_name', 'dept_print']


def get_student_info(std_no, keys=INFO_KEYS):
    res = requests.post(NTUB_API_URL, std_no, headers=NTUB_API_HEADERS)
    if not res.ok or not res.json():
        raise AuthenticationFailed()

    data = {}
    for k, v in res.json()[0].items():
        key = k.replace('_', '')
        key = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
        key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
        data[key] = v

    if data.get('status') != '在學':
        raise AuthenticationFailed()

    return {k: v for k, v in data.items() if k in keys}
