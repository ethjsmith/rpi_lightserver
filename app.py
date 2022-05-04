
import flask_login, hashlib, datetime, subprocess, os, secret
from importlib import import_module
from flask import Flask, request, render_template, redirect, url_for, flash, Response, g, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUserMixin, confirm_login, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

from database import db,User, Comment, Post, Target, Anon

#Camera = import_module('camera_pi').Camera
ap = Flask(__name__)
ap.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
ap.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

ap.secret_key = secret.system()
conf = secret.config()
conf[0] = '-g ' + conf[0]


#db = SQLAlchemy(ap)
db.init_app(ap)
# hmm how odd
#db.create_all()
migrate = Migrate(ap,db)

login_manager = LoginManager()
login_manager.anonymous_user = Anon
login_manager.login_view = "login"
login_manager.login_message = u"Please log in"
login_manager.refresh_view = "reauth"
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

login_manager.setup_app(ap)


#this function generates a video stream for the /vid, and /video paths, for video streaming
def gen(camera):
# generates video stream
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def admin_required(f):
    def wrap(*args, **kwargs):
        if current_user.email == 'ethan@esmithy.net':
            return f(*args, **kwargs)
        else:
            print("user not authorized for this page ")
            return redirect("/mypage")
    wrap.__name__=f.__name__
    return wrap

def login_required_v2(f):
    def wrap(*args, **kwargs):
        if 'user' in request.args and 'password' in request.args:
            if api_login(request.args['user'],request.args['password']):
                return f(*args, **kwargs)
            else:
                return login_manager.unauthorized()
        elif not current_user.is_authenticated:
            return login_manager.unauthorized()
        return f(*args, **kwargs)
    wrap.__name__=f.__name__
    return wrap

def api_login(username, password):
    user = User.query.filter_by(email=username).first()
    if user != None:
        if username == user.email:
            if user.check_password(password):
                if login_user(user,remember=True):
                    flash("successful login for " + user.name,category='info')
                    return True
    return False


#Context processor makes functions and variable available to the app ( most importantly for my usage, the templates)
@ap.context_processor
def giveFunctions():
    def getPosts(url=None):
        if url is not None:
            posts = Post.query.filter_by(topic=url).order_by(Post.tstamp.desc()).all()
        else:
            posts = Post.query.all()
        return posts
    def getTopics():
        topics = Post.query.with_entities(Post.topic).distinct()
        return topics
    def getComments(z):
        comments = Comment.query.filter_by(article=z).order_by(Comment.tstamp.desc())
        return comments
    def getFiles():
        x=[]
        uploadedfiles= os.listdir('static/')
        for z in uploadedfiles:
            x.append(str(z))
        return x
    return dict(getPosts=getPosts,getTopics=getTopics,getComments=getComments,getFiles=getFiles)

# default homepage route
@ap.route("/")
def home():
    z = "user:" + current_user.name
    if isinstance(current_user,Anon):
        z += "<br>is anon"
    return render_template('genericpage.html',title="home",body="Welcome to the homepage")

# About route, this is a legacy page, which doesn't scale like the other pages :(
@ap.route('/About')
@login_required_v2
def about_page():
    k = "<h1>About Me</h1><br><p>My name is Ethan Smith, and I am a CSIS student at Southern Utah University. at SUU I am also the Vice President of the cyber defence (competition) club, and a student security analyst. I love programming ( prefer Python and Java), Snowboarding during the winter, and playing lots of different video games. I also enjoy homemade IOT devices, and <br> Contact me at `ethan@esmithy.net` </p> <p> About the site: <br> This site was built as a project, just something that I like to play around with when I have some downtime between work and school. I had the idea to make a website which instead of having static html files and PHP templates, would use python to generate all the pages by chaining together string variables containing bits of html, which altogether would generate web pages. I've done a lot of things to try and make the site scalable, instead of static, and I've really enjoyed putting it together, although writing html with python syntax highlighting can be a pain sometimes! </p>"
    return render_template('genericpage.html',title="About",body=k)

# registration route, for registering for a new user account...
@ap.route('/register', methods=["GET","POST"])
def register():
    if current_user.name != "Not Logged in":
        return redirect ("/mypage")
    if request.method == 'POST':
        if 'name' in request.form and 'password' in request.form and 'email' in request.form:
            new = User.query.filter_by(email=request.form['email']).first()
            if new == None:
                if request.form['password'] == request.form['password2']:
                    new = User(request.form['name'],request.form['password'],request.form['email'])
                    db.session.add(new)
                    db.session.commit()
                    flash("New user added",category='info')
                    return redirect('/login')
            else:
                flash("ERROR, invalid email address",category ='error')
    return render_template("register.html")

# login route, for existing users to login, also @login_required redirects here
@ap.route("/login", methods=["GET","POST"])
def login():
    if current_user.name != "Not Logged in":
        return redirect("/mypage")
    if request.method == "POST" and "username" in request.form:
        user = User.query.filter_by(email=request.form["username"]).first()
        if user != None:
            username = request.form["username"]
            pas = request.form["password"]
            if username == user.email:
                if user.check_password(pas):
                    if login_user(user,remember=True):
                        flash("successful login for " + user.name,category='info')
                        return redirect(request.args.get("next") or "/")
        flash("login failed, wrong username(email) or password",category ='error')
    return render_template("login.html")

# Logout route, to log users out, ending their session.
@ap.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logged out",category='info')
    return redirect("/")

# Protected route control , allows admin users to control the lights, and other radio devices connected to the web host
@ap.route('/control')
@login_required_v2
@admin_required
# the fan terminology is kind of unintuative, "cool" basically means "fan on" and "heat" means "fan off"... they match the invocation intents in the skill
def control():
    bdy = """   <a href='/control/go?arg=on'>Light On</a>   <br>
                <a href='/control/go?arg=off'>Light Off</a> <br>
                <a href='/control/go?arg=cool'>Fan On</a>   <br>
                <a href='/control/go?arg=heat'>Fan Off</a>  <br>
    """
    return render_template("genericpage.html",body=bdy)

# Protected NONPAGE route redirects control's output methods, running the actual scripts, and then redirecting back to the control page
@ap.route('/control/go')
@login_required_v2
#@login_required
@admin_required
def doEverything():
    if request.args.get('arg') != None:
        if request.args.get('arg') == "on":
            print("do thing 1")
            subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[1]])
        elif request.args.get('arg') == "off":
            print("do thing 2")
            subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[2]])
        elif request.args.get('arg') == "cool":
            print("do thing 3")
            subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[3]])
        elif request.args.get('arg') == "heat":
            print("do thing 4")
            subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[4]])
        else:
            print ("error?")
    return redirect('/control')

# this route is the actual video stream, the next one shows it
#TODO: learn more about the response class
@ap.route('/video')
@login_required
@admin_required
def video():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# protected route vid shows a video from the connected camera
@ap.route('/vid')
@login_required
@admin_required
# displays the video with other website contents
def vid():
    return render_template('stream.html')

# this method allows uploading files to the server's static file... I think it's probably a really bad idea, but I wanted to see if I could do it... also it allows for creating new articles
@ap.route('/files', methods = ['GET','POST'])
@login_required
def files():
    if request.method == 'POST':
        f=request.files['file']
        f.save('./static/' + secure_filename(f.filename))
    links = ""
    uploadedfiles= os.listdir('static/')
    for z in uploadedfiles:
        # some exceptions that shouldn't be visible
        if str(z) != "style.css" and str(z) != "favicon.png" and not str(z).startswith('.'):
            links = links + "<a href = \"static/" + z + "\" >" + z + "</a><br>"
    bdy = '<h1> File share </h1> <div class = \"card\"> <form method = \"POST\" enctype = \"multipart/form-data\"><input type = \"file\" name = \"file\" /><input type = \"submit\" value = \"upload file\"/></form></div><br><div class = \"card\">' + links + '</div></html>'
    return render_template("genericpage.html",body=bdy,title="File Share")

# delete a file in the list of file sharing section
# if you want to add a button to do this, that's pretty easy, there's an example of it
# in my test repo attached to the filesharing
@ap.route('/files/d/<path:filename>')
@login_required
@admin_required
def deletefile(filename):
    if os.path.exists('files/' + filename):
        os.remove('files/' + filename)
    return redirect('/files')

# admin route, allowing management of users, and posts/articles
@ap.route('/admin')
@login_required
@admin_required
def admin():
    users = User.query.all()
    return render_template("admin.html",title='admin',users=users)


# crete a new article
# Requires : login, admin
@ap.route('/create', methods=['GET','POST'])
@login_required
@admin_required
def create():
    if request.method == "POST":
        if request.form['title'] != "" and request.form['body'] != '' and request.form['picture'] != '.gitignore':
            # create the new article here :)
            if request.form['topic'] == '_newTopic':
                art = Post(topic = request.form['newTopic'],title=request.form['title'],picture='/static/' + request.form['picture'],body=request.form['body'])
            else:
                art = Post(topic = request.form['topic'],title=request.form['title'],picture='/static/' + request.form['picture'],body=request.form['body'])
            db.session.add(art)
            db.session.commit()
            flash("successfully created new article",category='info')
        else:
            flash("error, missing required portion, or using invalid Image",category='error')
    return render_template('addArticle.html')


# admin delete driver, used for deleting any kind of content on the site
# admin page redirects requests here
# Requires : Login, Admin

# special case for the @ admin decorator
@ap.route('/admin/<path:type>/<path:did>')
@login_required
@admin_required
def admin_delete(type,did):
    if type == "post":
        Comment.query.filter_by(article=did).delete()
        Post.query.filter_by(id=did).delete()
        db.session.commit()
    elif type == "user":
        cmt = Comment.query.filter_by(poster=did).all()
        for c in cmt:
            c.poster = 1
            c.postername = "~Deleted User~"
        User.query.filter_by(id=did).delete()
        db.session.commit()
    elif type == "comment":
        Comment.query.filter_by(id=did).delete()
        db.session.commit()
    else :
        print("ERROR while trying to delete :" + type +","+ did)
    db.session.commit()
    return redirect(request.referrer or '/admin')


# a delete function for users to delete their own comments

@ap.route('/deletecomment/<path:cid>')
@login_required
def user_delete_comment(cid):
    canDelete = False
    if current_user.permission >= 10:
        canDelete = True
    else:
        e = Comment.query.filter_by(id=cid).first()
        if e.poster == current_user.id:
            canDelete = True
    if canDelete:
        nextd = Post.query.filter_by(id=e.article).first()
        db.session.delete(e)
        db.session.commit()
        return redirect('/' + nextd.topic + '/' + str(nextd.id))
    return redirect('/')


#This page is for a user to modify their own account
@ap.route('/mypage', methods=["GET","POST"])
@login_required
def userpage():
    if request.method == "POST":
        if request.form['username'] != '':
            flash("username updated",category='info')
            zz = Comment.query.filter_by(poster=current_user.id).all()
            for z in zz:
                z.postername = request.form['username']
            current_user.name = request.form['username']
        # Update passwords
        if request.form['password'] != '':
            if request.form['password'] == request.form['password2']:
                flash("password updated",category='info')
                current_user.change_password(request.form["password"])
            else:
                flash("Error, passwords don't match",category ='error')
        # Update email
        if request.form['email'] != '':
            q= db.session.query(User.id).filter_by(email=request.form['email']).first()
            if q is not None:
                flash('error, invalid email( or already in use)',category ='error')
            else:
                current_user.email = request.form['email']
                flash("Email updated",category='info')
        db.session.commit()

    return render_template('userManage.html')

#This section is the driver for all headings( article summaries)
#TODO: make only the first paragraph appear : )
@ap.route("/<path:url>")
def topic(url):
    posts = Post.query.filter_by(topic=url).all()
    if posts:
        for p in posts:
            print(p.tstamp)
        return render_template("list.html",title = url, articles = posts)
    addAttack(request.url)
    return render_template("genericpage.html",body="Topic not found!",title="Error")

@ap.route('/attacks', methods=["GET","POST"])
@login_required
def attacks():

    if request.method == "POST" and request.form["date"] != "":
        d = request.form['date'].split(",")
        y = datetime.datetime(int(d[2]),int(d[0]),int(d[1]))
        next = y + datetime.timedelta(days = 1)
        returns = Target.query.filter(Target.tstamp >= y).filter(Target.tstamp <= next)
    else:
        y=datetime.date.today() - datetime.timedelta(days  = 1)
        returns = Target.query.filter(Target.tstamp >= y)
    retme = ""
    for x in returns:
    	retme += 'at '+ x.time + "::" + x.data + "<br>"
    return render_template("attacks.html",body=retme,title='Recent attacks!',current=y,options=db.session.query(extract("month",Target.tstamp), extract("day",Target.tstamp), extract("year",Target.tstamp)).distinct())

@ap.route("/attacks/purge")
@login_required
def attack2():
    # removes all data older than 60 days
    n = datetime.datetime.today() - datetime.timedelta(days = 60)
    tgts = Target.query.filter(Target.tstamp < n).delete()
    db.session.commit()
    return redirect("/attacks")
# This section is the driver for all generic article pages
@ap.route("/<path:url>/<path:url2>",methods=["GET","POST"])
def artcle(url,url2):
    if request.method == "POST":
        if 'title' in request.form and 'message' in request.form:
            z = Comment(title=request.form['title'],message=request.form['message'],poster=current_user.id,postername = current_user.name, article=url2)
            db.session.add(z)
            db.session.commit()
    post = Post.query.filter_by(topic=url,id=url2).first()
    if post:
        return render_template("article.html",art = post,title=post.title,pidd=post.id)
    addAttack(request.url)
    return render_template("genericpage.html",body="Article not found!",title="Error")

def addAttack(url):
    n = Target(url)
    db.session.add(n)
    db.session.commit()

# actually runs the program
if (__name__ == "__main__"):
    ap.run()
