from flask import Flask, render_template
import requests

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('RAWG_API_KEY')

app = Flask(__name__)
@app.route('/')
def home():
    url = f'https://api.rawg.io/api/games?key={API_KEY}&page_size=20'
    response = requests.get(url)
    data = response.json()
    games = data.get('results', [])
    return render_template('index.html', games=games)

if __name__ == '__main__':
    app.run(debug=True)
