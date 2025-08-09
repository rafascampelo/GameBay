from flask import Flask, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()
API_KEY = os.getenv('RAWG_API_KEY')

app = Flask(__name__)

@app.route('/')
def home():
    """Rota principal que serve a página HTML estática."""
    return render_template('index.html')

@app.route('/api/games')
def get_games():
    """
    Rota que busca os jogos da API RAWG e retorna-os em formato JSON.
    Esta é a rota que o frontend irá chamar.
    """
    if not API_KEY:
        # Retorna um erro se a chave da API não estiver configurada
        return jsonify({'error': 'Chave da API RAWG não configurada.'}), 500

    url = f'https://api.rawg.io/api/games?key={API_KEY}&page_size=20'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro se a requisição falhar
        data = response.json()
        games = data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar jogos da API RAWG: {e}")
        return jsonify({'error': 'Erro ao buscar dados da API RAWG.'}), 500

    return jsonify(games)

if __name__ == '__main__':
    app.run(debug=True)
