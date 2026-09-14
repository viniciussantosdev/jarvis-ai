import ollama
import os
from datetime import datetime
from config import NOME_USUARIO

MODELO = "llama3.2:3b"
PASTA_RESPOSTAS = "respostas"
LIMITE_CARACTERES = 1000

PROMPT_SISTEMA = f"""Você é o Jarvis, um assistente pessoal de inteligência artificial, 
inspirado no assistente do Tony Stark. Você é educado, eficiente, levemente formal, 
e sempre se dirige ao usuário como "Senhor {NOME_USUARIO}". Responda de forma clara e 
direta. Suas respostas serão faladas em voz alta, então evite usar formatação como 
asteriscos, listas numeradas ou símbolos - prefira frases corridas e naturais, a menos 
que o usuário peça explicitamente por uma lista ou código.

Você tem acesso a ferramentas para executar ações específicas (abrir aplicativos, abrir 
sites, tocar música, buscar notícias). Use essas ferramentas APENAS quando o usuário pedir 
explicitamente para realizar essa ação. Para perguntas de conhecimento geral, curiosidades, 
cálculos, ou qualquer coisa que você já sabe responder, responda diretamente em texto, 
sem usar nenhuma ferramenta."""

historico = [
    {"role": "system", "content": PROMPT_SISTEMA}
]

def pensar(pergunta):
    historico.append({"role": "user", "content": pergunta})

    try:
        resposta = ollama.chat(
            model=MODELO,
            messages=historico,
            keep_alive= -1
        )
        texto_resposta = resposta["message"]["content"]
        historico.append({"role": "assistant", "content": texto_resposta})
        return texto_resposta

    except Exception as erro:
        print(f"Erro ao conectar com o Jarvis: {erro}")
        return "Desculpe, não consegui processar isso agora. Verifique se eu estou em execução"

def resumir_noticias(lista_noticias):
    texto_noticias = "\n".join(lista_noticias)

    prompt = f"""Aqui estão as principais notícias de hoje:

{texto_noticias}

Resuma essas notícias em um parágrafo curto e natural para ser falado em voz alta, 
como um boletim informativo rápido. Não use listas nem formatação, apenas frases 
corridas. Seja conciso, cobrindo os pontos principais de cada notícia."""

    mensagens = [
        {"role": "system", "content": PROMPT_SISTEMA},
        {"role": "user", "content": prompt}
    ]

    try:
        resposta = ollama.chat(
            model=MODELO,
            messages=mensagens,
            keep_alive= -1
        )
        return resposta["message"]["content"]
    except Exception as erro:
        print(f"Erro ao resumir notícias: {erro}")
        return "Encontrei as notícias, mas não consegui resumi-las agora, Senhor."
FERRAMENTAS = [
    {
        "type": "function",
        "function": {
            "name": "abrir_aplicativo",
            "description": "Abre um programa/aplicativo instalado no computador do usuário",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_app": {
                        "type": "string",
                        "description": "Nome do aplicativo a ser aberto, ex: spotify, vscode, chrome"
                    }
                },
                "required": ["nome_app"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "abrir_site",
            "description": "Abre um site ou faz uma busca no navegador",
            "parameters": {
                "type": "object",
                "properties": {
                    "termo_busca": {
                        "type": "string",
                        "description": "O que buscar ou qual site abrir, ex: youtube, 'receita de bolo no google'"
                    }
                },
                "required": ["termo_busca"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tocar_musica",
            "description": "Toca uma música no Spotify. Se o usuário pedir a musica favorita do Jarvis, use 'Should I Stay or Should I go'",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_musica": {
                        "type": "string",
                        "description": "Nome da música a ser tocada"
                    }
                },
                "required": ["nome_musica"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_noticias",
            "description": "Buscar as notícias mais recentes",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

def decidir_acao(pergunta):
    mensagens = [
        {"role": "system", "content": PROMPT_SISTEMA},
        {"role": "user", "content": pergunta}
    ]
    try:
        resposta = ollama.chat(
            model=MODELO,
            messages=mensagens,
            tools=FERRAMENTAS,
            keep_alive= -1
        )

        mensagem = resposta["message"]

        if "tool_calls" in mensagem and mensagem["tool_calls"]:
            chamada = mensagem["tool_calls"][0]
            nome_funcao = chamada["function"]["name"]
            argumentos = chamada["function"]["arguments"]
            return {"tipo": "acao", "funcao": nome_funcao, "argumentos": argumentos}

        texto_resposta = mensagem["content"]
        return {"tipo": "texto", "conteudo": texto_resposta}
    except Exception as erro:
            print(f"Erro ao conectar com o Jarvis: {erro}")
            return {"tipo": "texto", "conteudo":"Desculpe, não consegui processar isso agora."}

PALAVRAS_ACAO = ["abr", "toca", "toque", "pesquis", "busca", "buscar", "notícia", "noticia", "música", "musica"]

def parece_pedido_de_acao(texto):
    texto = texto.lower()
    return any(palavra in texto for palavra in PALAVRAS_ACAO)

def processar(pergunta):
    if parece_pedido_de_acao(pergunta):
        resultado = decidir_acao(pergunta)
        if resultado["tipo"] == "acao":
            return resultado

    texto_resposta = pensar(pergunta)
    return {"tipo": "texto", "conteudo": texto_resposta}

def limpar_memoria():
    global historico
    historico = [
        {"role": "system", "content": PROMPT_SISTEMA}
    ]

def resposta_longa(texto):
    return len(texto) > LIMITE_CARACTERES or "```" in texto

def salvar_em_arquivo(texto):
    if not os.path.exists(PASTA_RESPOSTAS):
        os.makedirs(PASTA_RESPOSTAS)

    nome_arquivo = f"{PASTA_RESPOSTAS}/resposta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)

    return nome_arquivo

if __name__ == "__main__":
    print("Teste de decisão (digite 'sair' pra encerrar)")
    while True:
        pergunta = input("Você: ")
        if pergunta.lower() == "sair":
            break

        resultado = processar(pergunta)

        if resultado["tipo"] == "acao":
            print(f"[AÇÃO DETECTADA] Função: {resultado['funcao']} | Argumentos: {resultado['argumentos']}")
        else:
            print(f"Jarvis: {resultado['conteudo']}")