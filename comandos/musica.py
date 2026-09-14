import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

ID_MUSICA_FAVORITA = "39shmbIHICJ2Wxnk1fPSdz"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state"
))

def eh_pedido_de_favorita(texto):
    texto = texto.lower()
    gatilhos = ["favorita", "should i stay", "should i go", "the clash"]
    return any(gatilho in texto for gatilho in gatilhos)

def tocar_musica(nome_musica):
    print(f"[DEBUG] nome_musica recebido: '{nome_musica}'")
    try:
        if not nome_musica or eh_pedido_de_favorita(nome_musica):
            print("[DEBUG] Entrou no branch: FAVORITA (ID fixo)")
            uri = f"spotify:track:{ID_MUSICA_FAVORITA}"
            faixa = sp.track(ID_MUSICA_FAVORITA)
            nome_encontrado = faixa["name"]
            artista = faixa["artists"][0]["name"]
        else:
            print(f"[DEBUG] Entrou no branch: BUSCA, termo='{nome_musica}'")
            resultados = sp.search(q=nome_musica, type="track", limit=1)
            faixas = resultados["tracks"]["items"]
            print(f"[DEBUG] Faixas encontradas: {[f['name'] + ' - ' + f['artists'][0]['name'] for f in faixas]}")

            if not faixas:
                return f"Não encontrei a música {nome_musica}, Senhor."

            faixa = faixas[0]
            uri = faixa["uri"]
            nome_encontrado = faixa["name"]
            artista = faixa["artists"][0]["name"]

        dispositivos = sp.devices()
        if not dispositivos["devices"]:
            return "Não encontrei nenhum dispositivo Spotify ativo, Senhor. Abra o Spotify primeiro"

        device_id = dispositivos["devices"][0]["id"]
        sp.start_playback(device_id=device_id, uris=[uri])

        return f""

    except Exception as erro:
        print(f"Erro ao tocar música: {erro}")
        return "Não consegui tocar a música agora, Senhor."