import os
SQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

ES = {
    'hosts': 'elasticsearch',
    'port': 9200,
    'http_auth': f"{os.getenv('ELASTICSEARCH_USERNAME')}:{os.getenv('ELASTIC_PASSWORD')}"
}

