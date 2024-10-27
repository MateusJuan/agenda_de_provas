import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir,"provas.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class prova(db.Model):
    materia = db.Colum(db.String(80),unique=True ,null=False, primary_key=True)

    def __repr__(self):
        return "<Materia {}>".format(self.materia)
    
@app.route('/', methods=["GET" , "POST"])
def home():
    provas = None #None ou ""
    if request.form:
        try:
            provas = prova(materia=request.form.get("Matéria"))
            db.session.add(prova)
            db.session.commit()
        except Exception as e:
            print("Falha ao adicionar prova")
    provas = prova.query.all()
    return render_template("index.html", provas=provas)

@app.route("/update", methods=["POST"])
def update():
    try:
        novamateria = request.form.get("Nova Matéria")
        antigamateria = request.form.get("Matéria Antiga")
        prova = prova.query.filter_by(materia=antigamateria).first()
        prova.materia = novamateria
        db.session.commit()
    except Exception as e:
        print("Falha ao atualizar")
        return redirect("/")
    
@app.route("/delete",methods=["POST"])
def delete():
    materia = request.form.get("Matéria")
    prova = prova.query.filter_by(materia=materia).first()
    db.session.delete(prova)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    