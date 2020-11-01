import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect


from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "tododatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Todo(db.Model):
    task = db.Column(db.String(200), nullable=False)
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    
    def __repr__(self):
        return "<Task: {}>".format(self.task)
    


@app.route("/")
def home():
    list2 = Todo.query.all()
    return render_template("app.html", list3=list2)
    
@app.route("/add", methods=["POST", "GET"])
def add():
    if request.form:
        work = Todo(task=request.form.get("task1"))
        db.session.add(work)
        db.session.commit()
        return redirect("/") 
    else:   
        return render_template("add.html")
        
@app.route("/edit/<id>/", methods=["POST", "GET"])
def edit(id):
    updated = Todo.query.get(id)
    if request.form:
        i = Todo.query.get(id)
        i.task = request.form.get("task2")
        db.session.add(i)
        db.session.commit()
        return redirect("/")        
    return render_template("edit.html", a=updated)
 
@app.route("/delete/<id>/", methods=["GET", "POST"])
def delete(id):
    i = db.session.query(Todo).filter(Todo.id == id).one()
    db.session.delete(i)
    db.session.commit()
    return redirect("/")
	
    
    
if __name__ == "__main__":
    app.run(debug=True)