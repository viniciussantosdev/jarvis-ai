from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

NOME_USUARIO = "Vinicius"
CAMINHO_VSCODE = r"C:\Users\2007v\AppData\Local\Programs\Microsoft VS Code\Code.exe"
CAMINHO_CLAUDE = r"C:\Users\2007v\AppData\Local\AnthropicClaude\claude.exe"
CAMINHO_SPOTIFY = r"C:\Users\2007v\AppData\Roaming\Spotify\Spotify.exe"


def saudacao():
    return f"Senhor {NOME_USUARIO}"
