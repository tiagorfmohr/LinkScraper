import os
from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Caminho para o diretório onde o arquivo HTML está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rota para servir o arquivo HTML
@app.route('/')
def serve_html():
    return send_from_directory(BASE_DIR, 'index.html')

# Função para raspar links da página
def scrape_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
        return links
    except Exception as e:
        return str(e)

# Rota para fazer a raspagem
@app.route('/scrape')
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400
    
    # Chama a função de raspagem e retorna os links encontrados
    links = scrape_links(url)
    if isinstance(links, str):  # Caso haja algum erro, como uma exceção
        return jsonify({'error': links}), 500
    
    return jsonify({'links': links})

# Rota principal para rodar o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
