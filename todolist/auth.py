from flask import Blueprint, render_template, request,  session, redirect, flash, url_for
from werkzeug.security import (generate_password_hash,check_password_hash)
from models import User
from __init__ import db

from flask_login import login_user,current_user, logout_user,login_required

auth = Blueprint('auth', __name__)
 
# Register form:
@auth.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect('/todo')
  if request.method =='POST':
    name=request.form.get('name')
    username=request.form.get('username')
    password=request.form.get('password')
    confirm=request.form.get('confirm')
    user = User.query.filter_by(username=username).first()
    if user:
      flash("username already exist","danger")
      return redirect(url_for('register' ))
     # create a new user with the form data. Hash the password so the text version isn't saved.
    new_user=User(name=name,username=username,password=generate_password_hash(password, method='sha256'))
    
    db.session.add(new_user)
    db.session.commit()
    flash("You've successfully registered!","success")
    return redirect('/login')
  return render_template('register.html') 

  
# login form
@auth.route('/login',methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect('/todo')

  if request.method=='POST':
    username=request.form['username']
    password=request.form['password'] 
    user= User.query.filter_by(username =username).first()
    if not user or not check_password_hash(user.password, password):
      
      flash('Please check your login details and try again.','danger')
      # if the user doesn't exist or password is wrong, reload the page
      return redirect(url_for('/login'))
    login_user(user, remember=True)
    flash('login successfully','success')
    return redirect(url_for('main.todo'))
   
   
    
  return render_template('login.html')  

#logout form:
@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash ("logout successfully","success")
  return redirect('/login')