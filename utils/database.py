import duckdb
import os

# Define o caminho do banco de dados dentro da pasta 'db'
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'games.duckdb')

def get_connection():
  """Retorna uma conexão com o DuckDB."""
  con = duckdb.connect(database=DB_PATH, read_only=False)
  return con

def setup_database():
  """Cria a tabela de favoritos se ela ainda não existir."""
  con = get_connection()
  # A tabela de favoritos guardará os dados importantes para a recomendação
  con.execute("""
      CREATE TABLE IF NOT EXISTS favoritos (
          game_id VARCHAR PRIMARY KEY,
          name VARCHAR,
          genres VARCHAR,
          tags VARCHAR
      );
  """)
  con.close()

def add_favorite(game_id, name, genres, tags):
  """Adiciona um jogo à tabela de favoritos."""
  con = get_connection()
  # Usa 'params' para evitar SQL Injection e garantir que a inserção seja segura
  try:
    con.execute("""
      INSERT INTO favoritos (game_id, name, genres, tags) VALUES (?, ?, ?, ?)
      ON CONFLICT (game_id) DO NOTHING;
    """, [game_id, name, genres, tags])
    con.close()
    return True
  except duckdb.Error as e:
    print(f"Erro ao adicionar favorito: {e}")
    con.close()
    return False

# Chama a função para criar a tabela quando o módulo é importado
setup_database()