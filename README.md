# 🎵 Spotify to MP3 Downloader Avançado

Um script robusto desenvolvido em Python para extrair playlists e faixas do Spotify e realizar o download automático em MP3 (320kbps). 

Para contornar as proteções de DRM do Spotify e garantir a máxima qualidade de áudio, este sistema utiliza uma arquitetura em duas etapas: ele consome a **API Oficial do Spotify** apenas para mapear os metadados (Artista e Nome da Música) e, em seguida, delega ao **yt-dlp** e ao **FFmpeg** a tarefa de buscar, baixar e converter o áudio silenciosamente via YouTube.

---

## ✨ Funcionalidades

- **Suporte Híbrido:** Extrai tanto faixas únicas (`/track/`) quanto playlists inteiras (`/playlist/`).
- **Alta Fidelidade:** Força o processamento do áudio para o formato `.mp3` na qualidade máxima de 320kbps.
- **Bypass de Limites de API:** Lida automaticamente com a paginação do Spotify, suportando playlists com centenas de músicas.
- **Tratamento de Exceções:** Ignora arquivos locais ou podcasts sem interromper o fluxo de download do resto da playlist.
- **Segurança de Credenciais:** Utiliza variáveis de ambiente (`.env`) para garantir que suas chaves de API nunca sejam expostas.

---

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes componentes instalados na sua máquina:

1. **[Python 3.x](https://www.python.org/downloads/)**
2. **Git** (Para clonar o repositório)
3. **FFmpeg** (Motor de conversão de áudio, obrigatório para gerar o MP3):
   - **Windows (via PowerShell):** `winget install ffmpeg`
   - **Linux (Debian/Ubuntu):** `sudo apt install ffmpeg`
   - **macOS (via Homebrew):** `brew install ffmpeg`

*(Nota: No Windows, após instalar o FFmpeg, pode ser necessário reiniciar o seu terminal ou a IDE para que o sistema reconheça o comando).*

---

## 🚀 Configuração Passo a Passo

### 1. Clonar o Repositório
Abra o seu terminal e clone o projeto para a sua máquina local:
```bash
git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
cd SEU_REPOSITORIO
