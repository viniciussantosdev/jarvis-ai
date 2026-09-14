# Jarvis — Assistente Pessoal de Voz

Assistente de voz local, inspirado no J.A.R.V.I.S. do universo Marvel, construído em Python com foco em rodar 100% no seu computador — sem depender de serviços pagos para o "cérebro" da IA.

## O que ele faz

- **Ativação por duas palmas ou pela palavra "Jarvis"**, com detecção robusta contra falsos positivos
- Conversa por voz, com memória de contexto durante a sessão
- Abre aplicativos e sites por comando de voz
- Toca músicas no Spotify (incluindo um easter egg com "Should I Stay or Should I Go", do The Clash)
- Busca e resume as notícias do dia
- Comandos de pausar/retomar e desligar por voz
- Abre automaticamente VS Code e Claude Desktop ao ativar
- Respostas longas ou com código são salvas em arquivo, em vez de faladas
- **Interface visual**: janela com orbe de partículas animado reagindo em tempo real (ouvindo, processando, falando), com transcrição da conversa
- **Ícone na bandeja do sistema**, com menu para mostrar/ocultar o painel, pausar e sair
- Roda como um programa real, via atalho `.bat`, sem precisar de terminal ou editor de código aberto

## Tecnologias

| Componente | Ferramenta |
|---|---|
| Reconhecimento de fala | `SpeechRecognition` (Google Speech API) |
| Síntese de voz | `edge-tts` |
| Cérebro / LLM | `Ollama` rodando `Llama 3.2 3B` localmente |
| Controle de música | `Spotipy` (API do Spotify) |
| Notícias | NewsAPI |
| Detecção de palmas | `sounddevice` + `numpy` |
| Interface gráfica | `tkinter` (orbe animado em Canvas) |
| Ícone de bandeja | `pystray` + `Pillow` |

## Arquitetura

O projeto roda em múltiplas threads coordenadas por filas (`Queue`):
- Thread de detecção de palmas
- Thread de detecção da wake word ("Jarvis")
- Thread de processamento de comandos (cérebro + ações)
- Thread do ícone de bandeja
- Thread principal, dedicada à interface gráfica (Tkinter)

A comunicação entre threads acontece via filas thread-safe, evitando acesso concorrente a recursos compartilhados (como o microfone) e mantendo a interface sempre responsiva.

## Pré-requisitos

- Python 3.10+
- [Ollama](https://ollama.com) instalado, com o modelo baixado:
  ```
  ollama pull llama3.2:3b
  ```
- Conta no [Spotify for Developers](https://developer.spotify.com/dashboard) (para tocar músicas)
- Chave de API do [NewsAPI](https://newsapi.org) (para notícias)

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/jarvis-ai.git
   cd jarvis-ai
   ```

2. Crie e ative o ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` na raiz do projeto com suas próprias credenciais:
   ```
   SPOTIFY_CLIENT_ID=seu_client_id
   SPOTIFY_CLIENT_SECRET=seu_client_secret
   NEWS_API_KEY=sua_chave_newsapi
   ```

5. No Spotify for Developers, configure o Redirect URI do seu app como:
   ```
   http://127.0.0.1:8888/callback
   ```

6. Ajuste os caminhos dos seus aplicativos em `config.py` (VS Code, Claude Desktop, Spotify) conforme a instalação do seu computador.

## Como usar

Duplo clique em `iniciar_jarvis.bat`, ou manualmente:
```
python main.py
```

O programa inicia direto na bandeja do sistema, sem abrir nenhuma janela. Clique com o botão direito no ícone para mostrar o painel visual, ocultá-lo, pausar o Jarvis ou encerrar.

Ative dizendo **"Jarvis"** ou batendo **duas palmas**, e fale seu comando.

### Alguns comandos de exemplo
- "Jarvis, abre o Spotify"
- "Jarvis, pesquisa receita de bolo no Google"
- "Jarvis, toca [nome de uma música]"
- "Jarvis, toca sua música favorita"
- "Jarvis, quais as notícias de hoje?"
- "Jarvis, desligar" / "Jarvis, dormir"
- "Jarvis, modo de espera" / "Jarvis, voltar"

### Iniciar automaticamente com o Windows (opcional)
Copie um atalho de `iniciar_jarvis.bat` para a pasta acessível via `Win + R` → `shell:startup`, para que o Jarvis inicie sozinho junto com o sistema.

## Estrutura do projeto

```
jarvis/
├── main.py            # Orquestra ativação, escuta, execução e interface
├── ativacao.py         # Detecção de palmas e wake word
├── ouvir.py            # Captura e transcrição de comandos
├── falar.py            # Síntese de voz
├── cerebro.py           # Integração com Ollama, memória e decisão de ações
├── interface.py          # Janela Tkinter com o orbe animado
├── bandeja.py            # Ícone e menu da bandeja do sistema
├── config.py             # Configurações e credenciais (lidas do .env)
├── comandos/
│   ├── apps.py         # Abrir aplicativos
│   ├── web.py          # Abrir sites e buscas
│   ├── musica.py        # Integração com Spotify
│   └── noticias.py       # Busca de notícias
└── iniciar_jarvis.bat    # Atalho de inicialização
```

## Limitações conhecidas

- Requer o Ollama e o Spotify abertos para funcionar por completo
- Modelo local (3B parâmetros) tem limitações de raciocínio comparado a LLMs maiores em nuvem
- Testado apenas em Windows

## Licença

Projeto pessoal, sem fins comerciais. Não afiliado à Marvel, Disney ou Anthropic.