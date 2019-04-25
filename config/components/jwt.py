from config.settings import env


JWT_ALGORITHM = 'HS256'

ACCESS_LIFETIME = env.int('ACCESS_LIFETIME')

REFRESH_LIFETIME = env.int('REFRESH_LIFETIME')
