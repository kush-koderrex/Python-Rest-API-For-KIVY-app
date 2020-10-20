from flask import Flask, render_template, request ,session,redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
# pip install -U Werkzeug==0.16.0
from datetime import datetime
from flask_mail import Mail
import os


# import json
# with open('config.json', 'r') as c:
#     params = json.load(c)["params"]
# local_server = True

app = Flask(__name__)
app.secret_key="super-secret-key"
app.config['UPLOAD_FOLDER']='F:\\kivy app for monu bahiya\\monu bhiya flask\\static\\img'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/koder'

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'jarvis.ai.kush@gmail.com',
    MAIL_PASSWORD=  '8979266654'
)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/koder"

db = SQLAlchemy(app)


# # ____________________________________________________________
# from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# # from flask_mail import Mail
# import json
# from datetime import datetime
#
#
# with open('config.json', 'r') as c:
#     params = json.load(c)["params"]
#
# local_server = True
#
# app = Flask(__name__)
#
# if(local_server):
#     app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
#
# db = SQLAlchemy(app)
# # _______________________________________________




class Contacts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    addres = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    contant = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/login",methods = ['GET', 'POST'])
def login():
    # ---------------session variable--------------
    if "user" in session and session['user'] == "koderrex":
        posts = Posts.query.all()
        return render_template('dashboard.html',posts=posts)


    if (request.method == 'POST'):
        username=request.form.get("uname")
        userpass=request.form.get("pass")
        if (username == "koderrex") and (userpass == "koder"):
            session['user'] = username
            posts=Posts.query.all()
            return render_template('dashboard.html',posts=posts)
    return render_template('login.html')

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', post=post)




@app.route("/edit/<string:sno>",methods = ['GET', 'POST'])
def edit(sno):
    if "user" in session and session['user'] == "koderrex":
        if request.method == "POST":
            box_title=request.form.get('tittle')
            contant=request.form.get('contant')
            slug=request.form.get('slug')
            img=request.form.get('img')
            date=datetime.now()
            if sno=='0':
                post=Posts(title=box_title,slug=slug,contant=contant,img=img,date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post=Posts.query.filter_by(sno=sno).first()
                post.title=box_title
                post.slug=slug
                post.contant=contant
                post.img=img
                post.date=date
                db.session.commit()
                return redirect("/edit/"+sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html',post=post)
        return "edit Succesfully"




@app.route("/uploader",methods = ['GET', 'POST'])
def uploader():
    if "user" in session and session['user'] == "koderrex":
        if (request.method == 'POST'):
            f=request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
            return "Uploaded Succesfully"



@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/login')

@app.route("/delete/<string:sno>",methods = ['GET', 'POST'])
def delete(sno):
    if "user" in session and session['user'] == "koderrex":
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')



@app.route("/contacts",methods = ['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_no=phone, addres=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender="email",
                          recipients=["jarvis.ai.kush@gmail.com"],
                          body = "Address:-"+"\n" + message + "\n" + str(phone))
        mail.send_message('Thank you for shopeing ' + name,
                          sender="jarvis.ai.kush@gmail.com",
                          recipients=[email],
                          body="Thank you for odering" + "\n" + name + "\n" + "Your order id is this :-")

    return render_template('contacts.html')


app.run(debug=True)

