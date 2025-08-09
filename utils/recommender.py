import requests
import os
import duckdb

# Importa a função de conexão do banco de dados
from .database import get_connection

def get_recommendations():
    """
    Gera recomendações de jogos baseadas nos jogos favoritos do usuário.
    """
    # 1. Conecta ao banco de dados e busca gêneros e tags dos jogos favoritos
    con = get_connection()
    favoritos = con.execute("SELECT genres, tags FROM favoritos;").fetchall()
    con.close()

    # Se não houver favoritos, não há como recomendar
    if not favoritos:
        return []

    # 2. Processa os dados para encontrar os gêneros e tags mais comuns
    generos_comuns = {}
    tags_comuns = {}

    for jogo in favoritos:
        # A informação está em string, precisamos dividi-la
        generos_jogo = jogo[0].split(', ')
        tags_jogo = jogo[1].split(', ')

        for genero in generos_jogo:
            generos_comuns[genero] = generos_comuns.get(genero, 0) + 1
        
        for tag in tags_jogo:
            tags_comuns[tag] = tags_comuns.get(tag, 0) + 1

    # Pega os 3 gêneros e as 5 tags mais frequentes
    generos_para_api = sorted(generos_comuns, key=generos_comuns.get, reverse=True)[:3]
    tags_para_api = sorted(tags_comuns, key=tags_comuns.get, reverse=True)[:5]
    
    # 3. Usa as informações para buscar novos jogos na RAWG API
    # Chaves da API
    API_KEY = os.getenv('RAWG_API_KEY')
    
    # Monta a URL da API de busca com os gêneros e tags mais populares
    url = f"https://api.rawg.io/api/games?key={API_KEY}"
    if generos_para_api:
        url += f"&genres={','.join(generos_para_api)}"
    if tags_para_api:
        url += f"&tags={','.join(tags_para_api)}"
    url += "&page_size=10" # Pega 10 jogos como recomendação
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Lança um erro para requisições com status 4xx/5xx
        dados_rawg = response.json()
        recomendacoes = dados_rawg.get('results', [])
        return recomendacoes
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar recomendações na RAWG API: {e}")
        return []
