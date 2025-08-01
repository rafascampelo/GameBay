from flask import Flask, render_template
import requests

app = Flask(__name__)

API_KEY = 'SUA_API_KEY_RAWG'  # Coloca aqui a tua key

@app.route('/')
def home():
    url = f'https://api.rawg.io/api/games?key={API_KEY}&page_size=20'
    response = requests.get(url)
    data = response.json()
    games = data.get('results', [])
    return render_template('index.html', games=games)

if __name__ == '__main__':
    app.run(debug=True)
