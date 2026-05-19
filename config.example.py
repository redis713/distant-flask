class Config:
    SECRET_KEY = 'secret'

    # Настройки MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/distant-flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False