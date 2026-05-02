

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/url_shortener"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    DEBUG = True

