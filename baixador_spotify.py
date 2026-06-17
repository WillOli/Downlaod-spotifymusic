import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp
import os

# ==========================================
# 1. CREDENCIAIS DA API DO SPOTIFY
# ==========================================
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Autenticação robusta via OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="playlist-read-private playlist-read-collaborative"
))


# ==========================================
# 2. FUNÇÕES DE METADADOS (SPOTIFY)
# ==========================================
def obter_metadados_track(url_track):
    """Extrai os dados de uma única música"""
    track_id = url_track.split('/')[-1].split('?')[0]
    track_info = sp.track(track_id)

    nome_musica = track_info['name']
    nome_artista = track_info['artists'][0]['name']

    return [f"{nome_artista} - {nome_musica}"], "Download_Avulso"


def obter_metadados_playlist(url_playlist):
    """Extrai todas as músicas de uma playlist corrigindo a chave do JSON"""
    playlist_id = url_playlist.split('/')[-1].split('?')[0]

    print("Conectando ao Spotify para ler a playlist...")
    playlist_info = sp.playlist(playlist_id)
    nome_playlist = playlist_info['name']

    nome_pasta = "".join(x for x in nome_playlist if x.isalnum() or x in " -_").strip()

    resultados = sp.playlist_tracks(playlist_id)
    faixas = resultados['items']

    while resultados['next']:
        resultados = sp.next(resultados)
        faixas.extend(resultados['items'])

    lista_buscas = []

    # Loop ajustado para lidar com a variação de chaves da API
    for i, elemento in enumerate(faixas):
        # A MÁGICA ACONTECE AQUI: Pega 'track' ou 'item'
        track = elemento.get('track') or elemento.get('item')

        if track is None:
            print(f"⚠️ Item {i} ignorado: Estrutura da música está realmente vazia.")
            continue

        if not track.get('name'):
            continue

        nome_musica = track['name']
        if track.get('artists') and len(track['artists']) > 0:
            nome_artista = track['artists'][0]['name']
        else:
            nome_artista = "Artista Desconhecido"

        lista_buscas.append(f"{nome_artista} - {nome_musica}")

    print(f"\nPlaylist '{nome_playlist}' mapeada! Total extraído: {len(lista_buscas)} músicas.")
    return lista_buscas, nome_pasta


# ==========================================
# 3. FUNÇÃO DE DOWNLOAD E CONVERSÃO (YT-DLP)
# ==========================================
def baixar_audio_youtube(lista_termos, nome_pasta):
    """Busca a lista de termos no YouTube e baixa o áudio na pasta"""
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)
        print(f"📁 Pasta criada: {nome_pasta}")

    caminho_saida = os.path.join(nome_pasta, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': caminho_saida,
        'default_search': 'ytsearch1:',
        'quiet': False,
        'no_warnings': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, termo in enumerate(lista_termos, 1):
            print(f"\n[{i}/{len(lista_termos)}] Processando: {termo}")
            try:
                ydl.download([termo])
            except Exception as e:
                print(f"⚠️ Erro ao baixar '{termo}': {e}. Pulando para a próxima...")


# ==========================================
# 4. FLUXO PRINCIPAL DE EXECUÇÃO
# ==========================================
if __name__ == "__main__":
    print("=== SPOTIFY DOWNLODER AVANÇADO ===")
    url_input = input("Cole a URL do Spotify: ").strip()

    try:
        if "/playlist/" in url_input:
            lista_musicas, pasta_destino = obter_metadados_playlist(url_input)

            if len(lista_musicas) > 0:
                baixar_audio_youtube(lista_musicas, pasta_destino)
                print(f"\n✅ Playlist concluída! Músicas salvas na pasta: {pasta_destino}")
            else:
                print("\n❌ Nenhuma música válida foi encontrada para download.")

        elif "/track/" in url_input:
            lista_musicas, pasta_destino = obter_metadados_track(url_input)
            baixar_audio_youtube(lista_musicas, pasta_destino)
            print("\n✅ Download da faixa concluído com sucesso!")

        else:
            print("❌ Erro: Link não reconhecido. Use links de 'playlist' ou 'track'.")

    except spotipy.exceptions.SpotifyException as e:
        print(f"\n❌ Erro na API do Spotify: {e}")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")