Flask user : a dynamic flask site with users, and a database to store both users and articles. (this is basically the staging/building area for a huge upgrade to rpi_lightserver)

(must be python3)
run `python vanilla.py`

required installs : Flask, flask_login, flask_sqlachemy

 ===TODO===
. moves sensitive information (secret_key) into an  external config not saved in GitHub
.restructure the various functions that require admin power to use ( like video?)
Standardize naming conventions ( specifically Post/Article)
improve ability to add paragraphs to articles ?
== BUGS ==
. better admin security ?
# deploy

==QOL==
. WTF forms
. db link between articles(/content) and users

== Minor ==
. generictemplate.html rework to markup object instead of `|safe` variable ( possible security)


==admin functionality==
.manage Users

currently you can create and load the database like this :
```python
from app import User,Post,Comment,Anon
from app import db

db.create_all()
#two example users
b = User(name='test',password='pass',email='test@b.c')
a = User(name='ethan',password='password',email='a',permission=999)
# add and save the users
db.session.add(a)
db.session.add(b)
db.session.commit()
#example of an article
p1 = Post(topic="misc",title="Example Article",picture="/static/Pic.jpg",body="This is the body of the article, which accepts <i> HTML tags </i>")
p2 = Post(topic="misc",title="Ex2",picture="/static/Pic.jpg",body="some random placeholder text here please")
p3 = Post(topic="a new topic appears",title="Example Article",picture="/static/Pic.jpg",body="I yote a duck off a cliff... turns out they can fly, so everything was fine")

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.commit()
#c = Comment(title='test',message='I love testing',poster="testman",article=1)
#db.session.add(c)
db.session.commit()
quit()
```
( this is literally the script I use to recreate the database every time I break it or have to make a migrating change )
