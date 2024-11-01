import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "provas.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Prova(db.Model):
    materia = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    assunto = db.Column(db.String(200), nullable=True)
    data = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return "<Materia {}, Assunto {}, Data {}>".format(self.materia, self.assunto, self.data)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_prova():
    if request.method == "POST":
        materia_input = request.form.get("materia")
        assunto_input = request.form.get("assunto")
        data_input = request.form.get("data")
        
        if materia_input and data_input:
            try:
                data_prova = datetime.strptime(data_input, "%Y-%m-%d").date()
                nova_prova = Prova(materia=materia_input, assunto=assunto_input, data=data_prova)
                db.session.add(nova_prova)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print("Falha ao adicionar prova:", e)
            return redirect(url_for("listar_provas"))
    return render_template("add_prova.html")

@app.route('/listar')
def listar_provas():
    provas = Prova.query.all()
    return render_template("listar_provas.html", provas=provas)

@app.route("/update", methods=["POST"])
def update():
    try:
        antigamateria = request.form.get("antigamateria")
        novamateria = request.form.get("novamateria")
        novoassunto = request.form.get("novoassunto")
        novadata = request.form.get("novadata")

        if novamateria and antigamateria:
            prova = Prova.query.filter_by(materia=antigamateria).first()
            if prova:
                prova.materia = novamateria
                prova.assunto = novoassunto
                prova.data = datetime.strptime(novadata, "%Y-%m-%d").date() if novadata else prova.data
                db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Falha ao atualizar:", e)
    return redirect(url_for("listar_provas"))

@app.route("/delete", methods=["POST"])
def delete():
    materia = request.form.get("materia")
    if materia:
        try:
            prova = Prova.query.filter_by(materia=materia).first()
            if prova:
                db.session.delete(prova)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Falha ao deletar:", e)
    return redirect(url_for("listar_provas"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
