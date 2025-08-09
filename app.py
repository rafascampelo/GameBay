from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Importa a função de banco de dados
from utils.database import add_favorite, setup_database
# Importa a função de recomendação
from utils.recommender import get_recommendations

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
API_KEY = os.getenv('RAWG_API_KEY')

app = Flask(__name__)

# Chama a função para garantir que a tabela de favoritos exista
setup_database()

@app.route('/')
def home():
    """Rota principal que exibe a página HTML."""
    return render_template('index.html')

@app.route('/api/games')
def get_games():
    """Nova rota que retorna a lista de jogos em formato JSON para o frontend."""
    url = f'https://api.rawg.io/api/games?key={API_KEY}&page_size=20'
    response = requests.get(url)
    data = response.json()
    games = data.get('results', [])
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

    if add_favorite(str(game_id), name, genres_str, tags_str):
        return jsonify({'success': True, 'message': f'Jogo "{name}" adicionado aos favoritos.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Jogo já está na lista ou ocorreu um erro.'}), 500

@app.route('/api/recommendations', methods=['GET'])
def get_game_recommendations():
    """Endpoint que retorna uma lista de jogos recomendados."""
    recomendacoes = get_recommendations()
    if not recomendacoes:
        return jsonify({'success': False, 'message': 'Não foi possível gerar recomendações. Adicione jogos favoritos primeiro.'}), 404
    
    return jsonify(recomendacoes), 200

@app.route('/api/search', methods=['GET'])
def search_games():
    """Novo endpoint que permite a pesquisa de jogos por nome."""
    query = request.args.get('q', '') # Pega o parâmetro 'q' da URL
    if not query:
        return jsonify({'success': False, 'message': 'Parâmetro de busca "q" é obrigatório.'}), 400
    
    url = f'https://api.rawg.io/api/games?key={API_KEY}&search={query}&page_size=10'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data.get('results', []))
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar jogos na RAWG API: {e}")
        return jsonify({'success': False, 'message': 'Erro ao buscar jogos. Tente novamente.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
