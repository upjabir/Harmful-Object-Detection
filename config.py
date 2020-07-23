import os
class Config:
    SECRET_KEY = 'mysecretkey'
    DEBUG=True


    basedir=os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME=os.environ.get('UNAME')
    MAIL_PASSWORD=os.environ.get('PASSWORD')

    