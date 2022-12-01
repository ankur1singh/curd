from flask import Flask
from flask import render_template,request,flash,redirect,session
from flask_login import LoginManager, login_user, logout_user



app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess' 
app.secret_key="abc"
app.config['SQLALCHEMY_DATABASE_URI']= "mysql+pymysql://sammy:password@localhost/registeration"

login_manager = LoginManager()

login_manager.init_app(app)
  
from models import db, User, Profile

db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/")
def index():
    data=Profile.query.all()
    return render_template("index.html",data=data)

@app.route("/forget",methods=['GET','POST'])
def forget():
    
    if request.method=='POST':
        email= request.form.get('email')
        user =User.query.filter_by(email=email).first_or_404()
        
        db.session.add(user)
        db.session.commit()

        flash('Check your Email','success')
    return render_template("forget.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':

        name=request.form.get('name')
        password=request.form.get('pswd')
        session['name']=request.form['name']
        if 'name' in session:
            s=session['name']
        user =User.query.filter_by(name=name).first()
        if user and password==user.password:
            login_user(user)
            
            return render_template("profile.html",s=s)
        else:
            flash('Invalid Creadentials','warning')
            return redirect('/login')

    return render_template("login.html")

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        mobile=request.form.get('mobile')
        password=request.form.get('pswd')
        user=User(name=name,email=email,mobile=mobile,password=password)
        db.session.add(user)
        db.session.commit()
        flash('user has been Registeresd successfully','success')
        return redirect('/login')

    return render_template("register.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/profile', methods=['GET','POST'])
def profile():
    if request.method=='POST':
        
        custId= request.form.get('custId')
        name= request.form.get('name')
        email= request.form.get('email')
        mobile= request.form.get('mobile')
        dob= request.form.get('dob')
        gender= request.form.get('gender')
        education= request.form.get('education')
        skill=request.form.get('skill')
        image= request.form.get('image')
        session['name']=request.form['name']
        if 'name' in session:
            s=session['name']
        profile=Profile(name=name,email=email,mobile=mobile,dob=dob,gender=gender,education=education,image=image,skill_id=skill,user_id=custId)
        db.session.add(profile)
        db.session.commit()
        flash('your profile is submit successfully','success')
        return redirect('/')
    return render_template("profile.html")

@app.route("/delete/<int:id>", methods=['GET','POST'])
def delete(id):
    profile=Profile.query.get(id)
    db.session.delete(profile)
    db.session.commit()
    flash('profile has been deleed','danger')
    return redirect('/')
    return render_template("profile_detail",profile=profile)

@app.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    profile=Profile.query.get(id)
    data=[{'gender': 'female'}, {'gender': 'male'}],
    if request.method=='POST':
        profile.name= request.form.get('name')
        profile.email= request.form.get('email')
        profile.mobile= request.form.get('mobile')
        profile.dob= request.form.get('dob')
        profile.gender= request.form.get('gender')
        profile.education= request.form.get('education')
        profile.image= request.form.get('image')
        db.session.commit()
        flash('profile has been updated','success')
        return redirect('/')
    return render_template("edit.html",profile=profile,data=data)

if __name__ == "__main__":

  app.run(debug = True,port=8080)