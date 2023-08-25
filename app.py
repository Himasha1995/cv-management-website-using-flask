from flask import Flask, request, url_for, flash,render_template, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import sqlite3
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'portfolio'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')



    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')


@app.route('/myresume')
def myresume():
    
    return render_template('myresume.html')

@app.route('/client-details')
def select():
	return render_template('client-details.html')



@app.route('/result', methods=['POST'])
def hello():
    name=request.form['yourname']
    email=request.form['youremail']
    contact=request.form['contact']
    fathername=request.form['fathername']
    address=request.form['address']
    residance=request.form['residance']
    dob=request.form['dob']
    lang=request.form['lang']
    gb=request.form['gb']
    gm=request.form['gm'] 
    gp=request.form['gp']
    gs=request.form['gs']

    tb=request.form['tb']
    tm=request.form['tm'] 
    tp=request.form['tp']
    ts=request.form['ts']
    tvb=request.form['tvb']
    tvm=request.form['tvm'] 
    tvp=request.form['tvp']
    tvs=request.form['tvs']	
    
    projetcs=request.form['projects'] 
    skills=request.form['skills']
    achievements=request.form['achievements']   
    return render_template('cv.html', name=name, email=email,contact=contact,dob = dob, lang = lang, address = address, fathername = fathername, residance = residance,gp=gp,gs=gs,gm=gm,gb=gb,tb=tb,tp=tp,tm=tm,ts=ts,tvb=tvb,tvm=tvm,tvp=tvp,tvs=tvs,projetcs = projetcs, skills = skills, achievements = achievements)

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)


@app.route('/template')
def template():
     return render_template('template.html')



@app.route('/contact', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':

        try:
            fname = request.form['fname']
            lname = request.form['lname']
         
            email = request.form['email']
            comment = request.form['comment']
            cur = mysql.connection.cursor()

            cur.execute("INSERT INTO details(fname,lname, email, comment) VALUES(%s,%s,%s,%s)",(fname,lname,email,comment))        
            mysql.connection.commit()

            # Close connection
            cur.close()
            flash('Your details are submitted, I will contact you soon, Thanks ', 'success')

            return redirect(url_for('index'))
        except Exception as e:
           return(str(e))
        
        return redirect(url_for('index'))
    return render_template('contact.html')

@app.route('/resume_1')
def resume_1():
    return render_template("resume_1.html")

@app.route('/resume_2')
def resume_2():
    return render_template("resume_2.html")

@app.route('/sample-resume')
def sampleresume():
    return render_template("sample-resume.html")

@app.route('/cv')
def resum():
    return render_template("cv.html")

@app.route('/resume_template')
def resume_template():
    return render_template("resume_template.html")


if __name__ == '__main__':
    app.run(debug=True)