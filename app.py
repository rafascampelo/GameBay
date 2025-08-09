from flask import Flask, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()
API_KEY = os.getenv('RAWG_API_KEY')

# Adiciona esta linha para verificar se a chave foi carregada
print(f"Chave da API RAWG carregada: {API_KEY}")
app = Flask(__name__)

@app.route('/')
def home():
    """Rota principal que exibe a página HTML."""
    return render_template('index.html')

@app.route('/api/games')
def get_games():
    """Rota que retorna a lista de jogos em formato JSON."""
    url = f'https://api.rawg.io/api/games?key={API_KEY}&page_size=20'
    response = requests.get(url)
    data = response.json()
    games = data.get('results', [])
    return jsonify(games)

if __name__ == '__main__':
    app.run(debug=True)
