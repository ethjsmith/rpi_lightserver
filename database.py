import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    '''User database model, created by new user (name,password,email)'''
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    comments = db.relationship('Comment', backref ='usr', lazy='dynamic', primaryjoin="User.id == Comment.poster")
    permission = db.Column(db.Integer)

    def __init__(self,name,password,email,permission=0):
        self.name = name
        self.password = self.set_password(password)
        self.email = email
        self.permission = permission
        if self.email == "ethan@esmithy.net": # this is kind of hacky :)
            self.permission = 999
    def is_active(self):
        return True
    def is_user(self):
        return False
    def is_authenticated(self):
        return True
    # save password as a hash instead of plaintext
    def set_password(self,password):
        return generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
# allows modification of user accounts
    def change_name(self, name):
        self.name = name
    def change_email(self,email):
        self.email = email
    def change_password(self,password):
        self.password = self.set_password(password)

class Comment(db.Model):
    '''Comment Database model, has more complicated foriegn keys, and so should only be created by the scripts attacked to the /?/? post route'''
    __tablename__ = "Comment"
    id= db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String())
    message = db.Column(db.String())
    poster = db.Column(db.Integer, db.ForeignKey('User.id'))
    postername = db.Column(db.String())
    date = db.Column(db.String())
    article = db.Column(db.Integer)
    tstamp = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    def __init__(self,title,message,poster,postername,article):
        self.title = title
        self.message = message
        self.poster = poster
        self.postername = postername
        self.article = article
        self.date = datetime.date.today().strftime('%b %d, %Y')

class Post(db.Model):
    __tablename__ = "Post"
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String())
    title = db.Column(db.String())
    picture = db.Column(db.String())
    body = db.Column(db.String())
    para = db.Column(db.String())
    date = db.Column(db.String())
    tstamp = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    def __init__(self,topic,title,picture,body):
        self.topic = topic
        self.title = title
        self.picture = picture
        self.body = body
        self.getFirstParagraph()
        self.date = datetime.date.today().strftime('%b %d, %Y')
    def getFirstParagraph(self):
        self.para = str(self.body.split("</p>")[0])
# This is the database entry for the data stored in the "attacks " page
class Target(db.Model):
    __tablename__ = "Target"
    id= db.Column(db.Integer, primary_key= True)
    data = db.Column(db.String())
    date = db.Column(db.String())
    time = db.Column(db.String())
    tstamp = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    def __init__(self,data):
        self.data = data
        self.date = datetime.date.today().strftime('%b %d, %Y')
        self.time = datetime.datetime.now().strftime('%H:%M')
    def __str__(self):
        return self.date
class Anon(AnonymousUserMixin):
    name = u"Not Logged in"
    permission = 0
