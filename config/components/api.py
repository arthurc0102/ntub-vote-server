from config.settings import env


NTUB_API_URL = 'https://msa.ntub.edu.tw:8081/api/SchoolSystem/Std_No/'
NTUB_API_TOKEN = env('NTUB_API_TOKEN')
NTUB_API_HEADERS = {
    'Authorization': 'Basic {}'.format(NTUB_API_TOKEN),
    'Content-Type': 'application/json',
}

GOOGLE_AUTH_API_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
GOOGLE_AUTH_VALID_HD = [
    'ntub.edu.tw',
]
