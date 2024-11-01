from flask import Flask, request, render_template, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)

# Configuração Supabase
SUPABASE_URL = "https://crmckdcgjcavmeiouoxl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNybWNrZGNnamNhdm1laW91b3hsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAzMDkzOTEsImV4cCI6MjA0NTg4NTM5MX0.i4zZ95r2AVHoXzJ-HDdpA_wgHMA5i1398ERFI1AYEbI"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

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
            prova_data = {
                "materia": materia,
                "assunto": assunto,
                "data": data
            }
            response = requests.post(f"{SUPABASE_URL}/rest/v1/provas", json=prova_data, headers=HEADERS)
            if response.status_code == 201:
                return redirect(url_for("listar_provas"))
            else:
                print("Falha ao adicionar prova:", response.json())
    return render_template("add_prova.html")

@app.route('/listar')
def listar_provas():
    response = requests.get(f"{SUPABASE_URL}/rest/v1/provas", headers=HEADERS)
    if response.status_code == 200:
        provas = response.json()
    else:
        provas = []
        print("Falha ao listar provas:", response.json())
    return render_template("listar_provas.html", provas=provas)

@app.route("/update", methods=["POST"])
def update():
    antigamateria = request.form.get("antigamateria")
    novamateria = request.form.get("novamateria")
    novoassunto = request.form.get("novoassunto")
    novadata = request.form.get("novadata")

    if novamateria and antigamateria:
        prova_data = {
            "materia": novamateria,
            "assunto": novoassunto,
            "data": novadata
        }
        response = requests.patch(f"{SUPABASE_URL}/rest/v1/provas?materia=eq.{antigamateria}", json=prova_data, headers=HEADERS)
        if response.status_code != 204:
            print("Falha ao atualizar prova:", response.json())
    return redirect(url_for("listar_provas"))

@app.route("/delete", methods=["POST"])
def delete():
    materia = request.form.get("materia")
    if materia:
        response = requests.delete(f"{SUPABASE_URL}/rest/v1/provas?materia=eq.{materia}", headers=HEADERS)
        if response.status_code != 204:
            print("Falha ao apagar prova:", response.json())
    return redirect(url_for("listar_provas"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)