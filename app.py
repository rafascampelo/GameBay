from flask import Flask, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()
API_KEY = os.getenv('RAWG_API_KEY')

app = Flask(__name__)

# Configura o DuckDB e cria a tabela de favoritos
# Supondo que tem um ficheiro utils/database.py com estas funções
# from utils.database import setup_database, add_favorite
# setup_database()

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

@app.route('/api/add_favorite', methods=['POST'])
def add_favorite_game():
    """Endpoint para adicionar um jogo à lista de favoritos."""
    data = request.json
    game_id = data.get('id')
    name = data.get('name')
    genres = [g['name'] for g in data.get('genres', [])]
    tags = [t['name'] for t in data.get('tags', [])]
    
    genres_str = ", ".join(genres)
    tags_str = ", ".join(tags)

    if not game_id or not name:
        return jsonify({'success': False, 'message': 'ID e nome do jogo são obrigatórios.'}), 400

    # Supondo que você tem a função add_favorite do DuckDB
    # if add_favorite(str(game_id), name, genres_str, tags_str):
    #     return jsonify({'success': True, 'message': f'Jogo "{name}" adicionado aos favoritos.'}), 200
    # else:
    #     return jsonify({'success': False, 'message': 'Jogo já está na lista ou ocorreu um erro.'}), 500

    # Placeholder para simular a lógica de adicionar aos favoritos
    return jsonify({'success': True, 'message': f'Jogo "{name}" adicionado aos favoritos.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
