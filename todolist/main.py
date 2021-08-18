from flask import Blueprint, render_template, session,request, redirect, flash, url_for, jsonify
from __init__ import create_app, db


from flask_login import current_user,login_required,login_user
from models import Todo,User

main = Blueprint('main', __name__)

import sqlite3 
import collections

@main.route('/home')
def home():
  return render_template('home.html')

#todo tasks:
@main.route('/todo/',methods=['POST','GET'])
@login_required
def todo():
  #todos=Todo.query.all()
  todos=Todo.query.filter_by(user_id=current_user.id).all()
  return render_template('todo.html',todos=todos)


#add form:
@main.route('/add',methods=['GET','POST'])
@login_required
def add():
    new_todo=Todo(title=request.form.get('title'),complete=False,user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    flash("new Todo has been added ","success")
    return redirect(url_for('main.todo'))
  
# update form:
@main.route('/update/<int:todo_id>')
@login_required
def update(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    todo.complete=not todo.complete
    db.session.commit()
    flash("Todo has been updated ","success")
    return redirect(url_for('main.todo'))

#Delete form:
@main.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
  with sqlite3.connect("todoapp.db") as con:
    cur = con.cursor()
    cur.execute("DELETE from todo where id = %s" % todo_id)
    con.commit()
    flash("Todo has been Deleted ","danger")
    return redirect(url_for('main.todo'))
    
# Get all todos as JSON form:
@main.route('/todo/json', methods = ['GET', 'POST'])

def get_json_data():
  with sqlite3.connect("todoapp.db") as con:
    cur = con.cursor()
    #cur.execute("SELECT * FROM  todo")
    cur.execute("SELECT * FROM  todo where user_id = %s" % current_user.id)
    rows=cur.fetchall()
    
    objects_list = []
    for row in rows:
      d = collections.OrderedDict()
      d['id'] = row[0]
      d['title'] = row[1]
      d['complete'] = row[2]
      objects_list.append(d)
    return jsonify(objects_list) 

 
app = create_app()
  
if __name__=='__main__':
  app.run(debug=True,port=5000,host='localhost')