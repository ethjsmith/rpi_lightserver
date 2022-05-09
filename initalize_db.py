from database import db, User,Post,Comment,Anon,Target
from werkzeug.security import generate_password_hash, check_password_hash
from app import ap
#from database import db

db.init_app(ap)
with ap.app_context():
    db.create_all()
    #two example users
    b = User(name='test',password='pass',email='test@b.c')
    a = User(name='ethan',password='password',email='a',permission=999)
    # add and save the users
    db.session.add(a)
    db.session.add(b)
    db.session.commit()
    #example of an article
    p1 = Post(topic='misc',title='Example Article',picture='/static/Pic.jpg',body='This is the body of the article, which accepts <i> HTML tags </i>')
    p2 = Post(topic='misc',title='Ex2',picture='/static/Pic.jpg',body='some random placeholder text here please')
    p3 = Post(topic='a new topic appears',title='Example Article',picture='/static/Pic.jpg',body='I yote a duck off a cliff... turns out they can fly, so everything was fine')

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.commit()
    #c = Comment(title='test',message='I love testing',poster='testman',article=1)
    #db.session.add(c)
    db.session.commit()
    quit()
