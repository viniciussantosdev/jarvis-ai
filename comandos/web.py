import webbrowser

SITES_CONHECIDOS = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "spotify": "https://spotify.com",
    "gmail": "https://gmail.com",
    "github": "https://github.com",
}

def abrir_sites(termo_busca):
    termo_busca = termo_busca.lower().strip()

    for nome_site, url in SITES_CONHECIDOS.items():
        if termo_busca == nome_site:
            webbrowser.open(url)
            return f"Abrindo {nome_site}."

    for nome_site, url in SITES_CONHECIDOS.items():
        if nome_site in termo_busca:
            resto_busca = termo_busca.replace(nome_site, "").strip()
            if resto_busca:
                if nome_site == "youtube":
                    url_final = f"{url}/results?search_query={resto_busca}"
                else:
                    url_final = f"https://google.com/search?q={termo_busca}"
                webbrowser.open(url_final)
                return f"Pesquisando {resto_busca} no {nome_site}"
            else:
                webbrowser.open(url)
                return f"Abrindo {nome_site}."
    url_google = f"https://google.com/search?q={termo_busca}"
    webbrowser.open(url_google)
    return f"Pesquisando {termo_busca} no Google"