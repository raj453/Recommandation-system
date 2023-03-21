from flask import Flask, request, render_template, redirect, url_for, session
from popularity.popularity import Rec_pop
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from endResult import result
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'



engine = create_engine('sqlite:///mydatabase.db', echo=True)
Session_db = sessionmaker(bind=engine)
Base = declarative_base()



db = SQLAlchemy(app)



class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    liked = db.Column(db.String(700))

Base.metadata.create_all(engine)
session_main = Session_db()

users = [
    {'username': 'john', 'password': generate_password_hash('password')},
    {'username': 'jane', 'password': generate_password_hash('1234')}
]



@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        df=Rec_pop()
        images = []
        for index, row in df.iterrows():
            data=row['imageURLHighRes']
            urls = data.split(',')
            first_url = urls[0]
            first_url=first_url.replace("'", "")
            if first_url.endswith("]"):
                first_url = first_url.rstrip("]")
            if first_url.endswith("'"):
                first_url = first_url.rstrip("'")
            if first_url.startswith("'"):
                first_url = first_url.lstrip("'") 
            if first_url.startswith("[]"):
                first_url = first_url.lstrip("[") 
            image = {'src': first_url[1:], 'title': row['title'], 'description': row['reviewText'],'id':row['productId']}
            images.append(image) 
        return render_template(
            "view.html",
            images=images
        )
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    img_url = url_for('static', filename='login.webp')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user2 = session_main.query(User).filter_by(username=username,password=password).first()
        user = next((user for user in users if user['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        elif user2:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password',img=img_url)
    else:
        return render_template('login.html',img=img_url)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    img_url = url_for('static', filename='login.webp')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if next((user for user in users if user['username'] == username), None) is None:
            
            new_user = User(username=username, password=password)
            global session_main 
            session_main= Session_db().add(new_user)
            session_main = Session_db().commit()


            users.append({'username': username, 'password': generate_password_hash(password)})
            session['username'] = username
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', error='Username already taken',img=img_url)
    else:
        return render_template('signup.html',img=img_url)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/single', methods=['GET', 'POST'])
def single():
    if 'username' in session:
        df=Rec_pop()
        df2=result()
        images = []
        name = request.args.get('param')
        user = session_main.query(User).filter_by(username=session['username']).first()
        user.liked=name

        
        for index, row in df2.iterrows():
            data=row['imageURLHighRes']
            urls = data.split(',')
            first_url = urls[0]
            first_url=first_url.replace("'", "")
            if first_url.endswith("]"):
                first_url = first_url.rstrip("]")
            if first_url.endswith("'"):
                first_url = first_url.rstrip("'")
            if first_url.startswith("'"):
                first_url = first_url.lstrip("'") 
            if first_url.startswith("["):
                first_url = first_url.lstrip("[") 
            image = {'src': first_url[1:], 'title': row['title'], 'description': row['reviewText'],'id':row['productId']}
            images.append(image) 
            
            
            if name is None:
                return "Please provide a name parameter"
            else:
                
                for index2, row2 in df.iterrows():
                        images3 = []
                        for index, row3 in df2.iterrows():
                            data=row3['imageURLHighRes']
                            urls3 = data.split(',')
                            first_url = urls3[0]
                            first_url=first_url.replace("'", "")
                            if first_url.endswith("]"):
                                first_url = first_url.rstrip("]")
                            if first_url.endswith("'"):
                                first_url = first_url.rstrip("'")
                            if first_url.startswith("'"):
                                first_url = first_url.lstrip("'") 
                            if first_url.startswith("["):
                                first_url = first_url.lstrip("[") 
                            image3 = {'src': first_url[1:], 'title': row3['title'], 'description': row3['reviewText'],'id':row3['productId']}
                            images3.append(image3)

                        
                        img_data=row2['imageURLHighRes']
                        urls = img_data.split(',')
                        first_url = urls[0]
                        first_url=first_url.replace("'", "")
                        if first_url.endswith("]"):
                            first_url = first_url.rstrip("]")
                        if first_url.endswith("'"):
                            first_url = first_url.rstrip("'")
                        if first_url.startswith("'"):
                            first_url = first_url.lstrip("'") 
                        if first_url.startswith("["):
                            first_url = first_url.lstrip("[") 
                        if row2['productId']==name:
                            data={'src': first_url[1:], 'title': row2['title'], 'description': row2['reviewText'],'id':row2['productId'],'summary':row2['summary']}
                            return render_template("single.html",images=images3 ,name=name,main=data,df_len=len)
                    
            
        return render_template(
            "single.html",
            images=images,
            name=name,
            main=images
        )
    else:
        return redirect(url_for('single'))

app.run(port=8080)