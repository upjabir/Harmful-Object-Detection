from mypackage import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(UserMixin,db.Model):
    __tablename__= 'users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15),unique=True)
    password=db.Column(db.String(200))
    email=db.Column(db.String(50),unique=True)

    def __init__(self, username, email,password):
        self.username=username
        self.email=email
        self.password=password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self,password):
        self.password=generate_password_hash(password,method='sha256')

    def check_password(self,password):
        return check_password_hash(self.password,password)


