import requests
from config import NEWS_API_KEY

import requests
from config import NEWS_API_KEY

def buscar_noticias():
    try:
        url = "https://newsapi.org/v2/everything"
        parametros = {
            "q": "Brasil",
            "language": "pt",
            "sortBy": "publishedAt",
            "pageSize": 5,
            "apiKey": NEWS_API_KEY
        }

        resposta = requests.get(url, params=parametros, timeout=10)
        dados = resposta.json()

        if dados.get("status") != "ok":
            return None

        artigos = dados.get("articles", [])

        if not artigos:
            return None

        noticias_formatadas = []
        for artigo in artigos:
            titulo = artigo.get("title", "")
            descricao = artigo.get("description", "")
            noticias_formatadas.append(f"{titulo}. {descricao}")

        return noticias_formatadas

    except Exception as erro:
        print(f"Erro ao buscar notícias: {erro}")
        return None