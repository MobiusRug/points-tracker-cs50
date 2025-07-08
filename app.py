from flask import Flask, render_template, request, redirect, jsonify, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
from datetime import datetime
from helpers import login_required

app = Flask(__name__)
# Updated secret key configuration using environment variable
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)

def get_db_connection():
    conn = sqlite3.connect('controle.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    conn = get_db_connection()
    user_id = session["user_id"]

    if request.method == "POST":
        try:
            protocolo = request.form.get("protocolo")
            especie = request.form.get("especie")
            pontos = float(request.form.get("pontos"))
            data_inclusao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            conn.execute(
                "INSERT INTO producao (protocolo, especie, pontuacao, data_inclusao, username_id) VALUES (?, ?, ?, ?, ?)",
                (protocolo, especie, pontos, data_inclusao, user_id)
            )
            conn.commit()
            flash("Registro adicionado com sucesso!", "success")
        except Exception as e:
            print("Erro ao salvar:", e)
            flash("Erro ao adicionar registro", "error")
            conn.rollback()
        finally:
            conn.close()
            return redirect("/")

    try:
        mes = request.args.get("mes")
        ano = request.args.get("ano")
        if not mes or not ano:
            agora = datetime.now()
            mes = agora.strftime("%m")
            ano = agora.strftime("%Y")

        tarefas = conn.execute("SELECT especie, pontos FROM pontuacao_referencia").fetchall()

        hoje = datetime.now().strftime('%Y-%m-%d')
        producao_hoje = conn.execute("""
            SELECT id, protocolo, especie, pontuacao, data_inclusao
            FROM producao
            WHERE DATE(data_inclusao) = ? AND username_id = ?
            ORDER BY data_inclusao DESC
        """, (hoje, user_id)).fetchall()
        total_hoje = sum(item["pontuacao"] for item in producao_hoje)

        producao_mes = conn.execute("""
            SELECT id, protocolo, especie, pontuacao, data_inclusao
            FROM producao
            WHERE strftime('%m', data_inclusao) = ? 
              AND strftime('%Y', data_inclusao) = ?
              AND username_id = ?
            ORDER BY data_inclusao DESC
        """, (mes, ano, user_id)).fetchall()
        total_mes = sum(item["pontuacao"] for item in producao_mes)

        producao_total = conn.execute("""
            SELECT id, protocolo, especie, pontuacao, data_inclusao
            FROM producao
            WHERE username_id = ?
            ORDER BY data_inclusao DESC
            LIMIT 50
        """, (user_id,)).fetchall()
        total_geral = sum(item["pontuacao"] for item in producao_total)

    except Exception as e:
        print("Erro ao buscar dados:", e)
        flash("Erro ao carregar dados", "error")
        return redirect("/login")
    finally:
        conn.close()

    return render_template(
        "index.html",
        tarefas=tarefas,
        producao_hoje=producao_hoje,
        total_hoje=total_hoje,
        producao_mes=producao_mes,
        total_mes=total_mes,
        mes=mes,
        ano=ano
    )

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    id = request.form.get("id")
    user_id = session["user_id"]
    
    if id:
        conn = get_db_connection()
        try:
            record = conn.execute(
                "SELECT id FROM producao WHERE id = ? AND username_id = ?",
                (id, user_id)
            ).fetchone()
            
            if record:
                conn.execute("DELETE FROM producao WHERE id = ?", (id,))
                conn.commit()
                flash("Registro removido com sucesso", "success")
                return jsonify({"success": True})
            return jsonify({"success": False, "error": "Não autorizado"})
        except Exception as e:
            print("Erro ao deletar:", e)
            flash("Erro ao remover registro", "error")
            return jsonify({"success": False, "error": str(e)})
        finally:
            conn.close()
    return jsonify({"success": False, "error": "ID inválido"})

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Preencha todos os campos", "error")
            return render_template("login.html")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user is None or not check_password_hash(user["hash"], password):
            flash("Usuário ou senha inválidos", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        flash(f"Bem-vindo, {username}!", "success")
        return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você foi desconectado", "info")
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password:
            flash("Preencha todos os campos", "error")
            return redirect("/register")

        if password != confirmation:
            flash("As senhas não coincidem", "error")
            return redirect("/register")

        hash_pwd = generate_password_hash(password)
        conn = get_db_connection()
        
        try:
            conn.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                (username, hash_pwd)
            )
            conn.commit()
            flash("Registro realizado com sucesso! Faça login.", "success")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Usuário já existe", "error")
            return redirect("/register")
        except Exception as e:
            flash(f"Erro no registro: {str(e)}", "error")
            return redirect("/register")
        finally:
            conn.close()
    
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=False)