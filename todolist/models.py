from __init__ import db
from flask_login import UserMixin


#create db Model:
class User(UserMixin,db.Model ):


  id = db.Column(db.Integer, primary_key=True)
  name=db.Column(db.String(200), unique=True)
  username=db.Column(db.String(200),unique=True )
  password=db.Column(db.String(80),unique=True)
  todos=db.relationship('Todo',backref='user')
  
  
  def _repr_(self):
        return f"User('{self.name}', '{self.username}', '{self.password}')"


  
  
class Todo(UserMixin,db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title=db.Column(db.String(100),unique=True)
  complete=db.Column(db.Boolean())
  user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
  
  

  def _repr_(self):
        return f"Todo('{self.title}','{self.complete}')"