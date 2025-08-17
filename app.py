from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import requests
import os
import sqlite3
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Importa as funções para a base de dados de jogos DuckDB
from utils.database import setup_games_db, add_favorite, get_favorites

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")

app = Flask(__name__)
# Define uma chave secreta para gerir as sessões do utilizador
app.secret_key = secrets.token_hex(16)


def get_db_connection():
    """Cria e retorna uma conexão com a base de dados de utilizadores (SQLite)."""
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def setup_user_database():
    """Cria a tabela de utilizadores se ela ainda não existir."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    """
    )
    conn.commit()
    conn.close()


# Configura as bases de dados ao iniciar a aplicação
setup_user_database()
setup_games_db()


@app.route("/")
def home():
    """Rota principal que serve a página HTML."""
    return render_template("index.html")


@app.route("/api/games")
def get_games():
    """Rota que busca os jogos da API RAWG e retorna-os em formato JSON."""
    if not API_KEY:
        return jsonify({"error": "Chave da API RAWG não configurada."}), 500

    url = f"https://api.rawg.io/api/games?key={API_KEY}&page_size=20"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        games = data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar jogos da API RAWG: {e}")
        return jsonify({"error": "Erro ao buscar dados da API RAWG."}), 500

    return jsonify(games)


@app.route("/register", methods=["POST"])
def register():
    """Rota para registar um novo utilizador."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Nome de utilizador e palavra-passe são obrigatórios.",
                }
            ),
            400,
        )

    conn = get_db_connection()
    try:
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()
        return (
            jsonify({"success": True, "message": "Utilizador registado com sucesso!"}),
            201,
        )
    except sqlite3.IntegrityError:
        return (
            jsonify(
                {"success": False, "message": "Este nome de utilizador já existe."}
            ),
            409,
        )
    finally:
        conn.close()


@app.route("/login", methods=["POST"])
def login():
    """Rota para autenticar um utilizador."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Nome de utilizador e palavra-passe são obrigatórios.",
                }
            ),
            400,
        )

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Login bem-sucedido!",
                    "username": user["username"],
                }
            ),
            200,
        )
    else:
        return jsonify({"success": False, "message": "Credenciais inválidas."}), 401


@app.route("/logout")
def logout():
    """Rota para terminar a sessão do utilizador."""
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/api/add_favorite", methods=["POST"])
def add_favorite_game():
    """Endpoint para adicionar um jogo à lista de favoritos, requer autenticação."""
    if "user_id" not in session:
        return (
            jsonify(
                {"success": False, "message": "Login necessário para favoritar jogos."}
            ),
            401,
        )

    data = request.json
    game_id = data.get("id")
    name = data.get("name")
    genres = [g["name"] for g in data.get("genres", [])]
    tags = [t["name"] for t in data.get("tags", [])]

    genres_str = ", ".join(genres)
    tags_str = ", ".join(tags)

    if not game_id or not name:
        return (
            jsonify(
                {"success": False, "message": "ID e nome do jogo são obrigatórios."}
            ),
            400,
        )

    if add_favorite(session["user_id"], str(game_id), name, genres_str, tags_str):
        return (
            jsonify(
                {"success": True, "message": f'Jogo "{name}" adicionado aos favoritos.'}
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Jogo já está na lista ou ocorreu um erro.",
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True)
