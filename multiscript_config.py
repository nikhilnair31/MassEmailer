# Broker settings.
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///articles.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
ARTICLES_PER_SITE_MIN = 0
ARTICLES_PER_SITE_MID = 1
ARTICLES_PER_SITE_MAX = 2

# AWS SES
AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY = 'AKIA6O5YE5GYSQQ4XVXQ'
AWS_SECRET_KEY = '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'

# AWS RDS
DB_URL = 'lgv3.cbgyqdzzm09b.ap-south-1.rds.amazonaws.com'
DB_USERNAME = 'test'
DB_PASSWORD = 'test123'
DB_PORT = 5432
DB_NAME = 'eml_test'

## CELERY AND REDIS
SVM_KERNEL = 'rbf'
SVM_GAMMA = 'auto'
SVM_CLASS_WEIGHTS = {0:1, 1:3}

#JS
AVG_READ_SPEED = 250 # words per minute

# LINKS
ANALYTICSVIDHYA_BASEURL = 'https://www.analyticsvidhya.com/?s='
MLMASTERY_BASEURL = 'https://machinelearningmastery.com/?s='
YOUTUBE_BASEURL = 'https://www.youtube.com/results?search_query='
WIKIPEDIA_BASEURL = 'https://en.wikipedia.org/wiki/'
MEDIUM_BASEURL = 'https://medium.com/search?q='