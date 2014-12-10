ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bikecompetition',
        'USER': 'bikecompetition_user',
        'PASSWORD': 'bikecompetition_password',
        'HOST': 'localhost',
        # 'PORT': '5432', #PostgreSQL 9.1
        #'PORT': '5433', #PostgreSQL 9.2
        'PORT': '5434',  #PostgreSQL 9.3
    }
}
