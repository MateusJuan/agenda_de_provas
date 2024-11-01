from flask import Flask, request, render_template, redirect, url_for
from supabase import create_client, Client
from datetime import datetime
import os

# Configure sua URL e chave do Supabase
SUPABASE_URL = 'https://crmckdcgjcavmeiouoxl.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNybWNrZGNnamNhdm1laW91b3hsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAzMDkzOTEsImV4cCI6MjA0NTg4NTM5MX0.i4zZ95r2AVHoXzJ-HDdpA_wgHMA5i1398ERFI1AYEbI'

app = Flask(__name__)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
                # Converte a data para string no formato ISO
                data_prova = datetime.strptime(data_input, "%Y-%m-%d").date().isoformat()
                nova_prova = {
                    "materia": materia_input,
                    "assunto": assunto_input,
                    "data": data_prova  # Agora é uma string
                }
                
                # Insere no Supabase
                response = supabase.table('provas').insert(nova_prova).execute()
                
                # Verifica se a inserção foi bem-sucedida
                if response.data:  # Se houver dados retornados
                    return redirect(url_for("listar_provas"))
                else:
                    print("Erro ao adicionar prova:", response.error)

            except Exception as e:
                print("Falha ao adicionar prova:", e)
                return "Erro ao adicionar prova", 500

    return render_template("add_prova.html")

@app.route('/listar')
def listar_provas():
    provas = supabase.table('provas').select('*').execute()
    return render_template("listar_provas.html", provas=provas.data)

@app.route("/update", methods=["POST"])
def update():
    try:
        antigamateria = request.form.get("antigamateria")
        novamateria = request.form.get("novamateria")
        novoassunto = request.form.get("novoassunto")
        novadata = request.form.get("novadata")

        if novamateria and antigamateria:
            updated_data = {
                "materia": novamateria,
                "assunto": novoassunto,
                "data": datetime.strptime(novadata, "%Y-%m-%d").date().isoformat() if novadata else None
            }
            response = supabase.table('provas').update(updated_data).eq('materia', antigamateria).execute()
            if response.error:
                print("Erro ao atualizar prova:", response.error)

    except Exception as e:
        print("Falha ao atualizar:", e)
    return redirect(url_for("listar_provas"))

@app.route("/delete", methods=["POST"])
def delete():
    materia = request.form.get("materia")
    if materia:
        try:
            response = supabase.table('provas').delete().eq('materia', materia).execute()
            if response.error:
                print("Erro ao Apagar:", response.error)

        except Exception as e:
            print("Falha ao Apagar:", e)
    return redirect(url_for("listar_provas"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)