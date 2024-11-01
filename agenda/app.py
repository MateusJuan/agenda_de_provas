from flask import Flask, request, render_template, redirect, url_for
from supabase import create_client, Client
from datetime import datetime

app = Flask(__name__)

# Configuração do Supabase
SUPABASE_URL = "https://crmckdcgjcavmeiouoxl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNybWNrZGNnamNhdm1laW91b3hsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAzMDkzOTEsImV4cCI6MjA0NTg4NTM5MX0.i4zZ95r2AVHoXzJ-HDdpA_wgHMA5i1398ERFI1AYEbI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_prova():
    if request.method == "POST":
        materia = request.form.get("materia")
        assunto = request.form.get("assunto")
        data = request.form.get("data")
        
        if materia and data:
            try:
                prova_data = {
                    "materia": materia,
                    "assunto": assunto,
                    "data": data
                }
                response = supabase.table("provas").insert(prova_data).execute()
                if response.status_code == 201:
                    return redirect(url_for("listar_provas"))
            except Exception as e:
                print("Falha ao adicionar prova:", e)
    return render_template("add_prova.html")

@app.route('/listar')
def listar_provas():
    try:
        response = supabase.table("provas").select("*").execute()
        provas = response.data
    except Exception as e:
        provas = []
        print("Falha ao listar provas:", e)
    return render_template("listar_provas.html", provas=provas)

@app.route("/update", methods=["POST"])
def update():
    antigamateria = request.form.get("antigamateria")
    novamateria = request.form.get("novamateria")
    novoassunto = request.form.get("novoassunto")
    novadata = request.form.get("novadata")

    if novamateria and antigamateria:
        try:
            prova_data = {
                "materia": novamateria,
                "assunto": novoassunto,
                "data": novadata
            }
            response = supabase.table("provas").update(prova_data).eq("materia", antigamateria).execute()
            if response.status_code != 204:
                print("Falha ao atualizar prova:", response.json())
        except Exception as e:
            print("Falha ao atualizar prova:", e)
    return redirect(url_for("listar_provas"))

@app.route("/delete", methods=["POST"])
def delete():
    materia = request.form.get("materia")
    if materia:
        try:
            response = supabase.table("provas").delete().eq("materia", materia).execute()
            if response.status_code != 204:
                print("Falha ao apagar prova:", response.json())
        except Exception as e:
            print("Falha ao apagar prova:", e)
    return redirect(url_for("listar_provas"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
