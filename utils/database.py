import duckdb
import os

# Define o caminho do banco de dados para os jogos
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'games.duckdb')

def get_games_db_connection():
  """Cria e retorna uma conexão com a base de dados de jogos."""
  con = duckdb.connect(database=DB_PATH, read_only=False)
  return con

def setup_games_db():
  """Cria a tabela de favoritos com uma coluna user_id."""
  con = get_games_db_connection()
  con.execute("""
      CREATE TABLE IF NOT EXISTS favoritos (
          game_id VARCHAR NOT NULL,
          user_id INTEGER NOT NULL,
          name VARCHAR,
          genres VARCHAR,
          tags VARCHAR,
          PRIMARY KEY (game_id, user_id)
      );
  """)
  con.close()

def add_favorite(user_id, game_id, name, genres, tags):
  """Adiciona um jogo à tabela de favoritos para um utilizador específico."""
  con = get_games_db_connection()
  try:
    con.execute("""
      INSERT INTO favoritos (user_id, game_id, name, genres, tags) VALUES (?, ?, ?, ?, ?)
      ON CONFLICT (game_id, user_id) DO NOTHING;
    """, [user_id, game_id, name, genres, tags])
    con.close()
    return True
  except duckdb.Error as e:
    print(f"Erro ao adicionar favorito: {e}")
    con.close()
    return False

def get_favorites(user_id):
  """Retorna todos os jogos favoritos de um utilizador específico."""
  con = get_games_db_connection()
  favorites = con.execute("SELECT * FROM favoritos WHERE user_id = ?;", [user_id]).fetchall()
  con.close()
  return favorites

# Chama a função para criar a tabela de jogos ao iniciar
setup_games_db()
