import subprocess
from config import CAMINHO_VSCODE, CAMINHO_CLAUDE, CAMINHO_SPOTIFY

APPS = {
    "spotify": CAMINHO_SPOTIFY,
    "vscode": CAMINHO_VSCODE,
    "vs code": CAMINHO_VSCODE,
    "claude": CAMINHO_CLAUDE,
    "chrome": "chrome",
    "navegador": "chrome"
}

def abrir_aplicativo(nome_app):
    nome_app = nome_app.lower().strip()

    if nome_app not in APPS:
        return f"Não encontrei o aplicativo {nome_app} na minha lista, Senhor."

    try:
        subprocess.Popen(APPS[nome_app])
        return f"Abrindo {nome_app}."
    except Exception as erro:
        print(f"Erro ao abrir {nome_app}: {erro}")
        return f"Não consegui abrir o {nome_app}, Senhor."