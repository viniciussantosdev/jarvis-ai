from ativacao import escutar_palmas, escutar_wake_word, pausar_escuta
from ouvir import ouvir_comando
from falar import falar
from cerebro import processar, resposta_longa, salvar_em_arquivo
from config import saudacao, CAMINHO_VSCODE, CAMINHO_CLAUDE
from comandos.apps import abrir_aplicativo
from comandos.web import abrir_sites
from comandos.musica import tocar_musica
from comandos.noticias import buscar_noticias
from cerebro import resumir_noticias
from interface import JanelaJarvis
from bandeja import BandejaJarvis
import threading
import queue
import sys
import subprocess

fila_ativacao = queue.Queue()
fila_interface = queue.Queue()

COMANDOS_DESLIGAR = ["desligar", "dormir", "encerrar"]
COMANDOS_PARAR = ["parar", "cancelar"]
COMANDOS_PAUSAR = ["modo de espera"]
COMANDOS_RETOMAR = ["voltar", "retomar", "pode continuar", "continuar"]

em_espera = False
programas_ja_abertos = False
janela_jarvis = None

def abrir_programas_iniciais():
    global programas_ja_abertos

    if programas_ja_abertos:
        return

    try:
        subprocess.Popen(CAMINHO_VSCODE)
    except Exception as erro:
        print(f"Erro ao abrir o VS Code: {erro}")

    try:
        subprocess.Popen(CAMINHO_CLAUDE)
    except Exception as erro:
        print(f"Erro ao abrir o Claude: {erro}")

    programas_ja_abertos = True

def executar_acao(funcao, argumentos):
    if funcao == "abrir_aplicativo":
        return abrir_aplicativo(argumentos.get("nome_app", ""))

    if funcao == "abrir_site":
        return abrir_sites(argumentos.get("termo_busca", ""))

    if funcao == "tocar_musica":
        return tocar_musica(argumentos.get("nome_musica", ""))

    if funcao == "buscar_noticias":
        noticias = buscar_noticias()
        if noticias is None:
            return "Não consegui buscar as notícias agora, Senhor. Verifique a conexão."
        resumo = resumir_noticias(noticias)
        return resumo

    return "Não consigo realizar esta ação, Senhor. Aguarde"

def mostrar_painel():
    if janela_jarvis:
        janela_jarvis.janela.deiconify()

def ocultar_painel():
    if janela_jarvis:
        janela_jarvis.janela.withdraw()

def alternar_pausa():
    global em_espera
    em_espera = not em_espera

def sair_do_programa():
    sys.exit(0)

def processar_comando():
    global em_espera

    while True:
        fila_ativacao.get()
        pausar_escuta.set()

        try:
            abrir_programas_iniciais()

            if em_espera:
                falar(f"Ainda em modo de espera, {saudacao()}.")
                comando = ouvir_comando()
                if comando and any(palavra in comando for palavra in COMANDOS_RETOMAR):
                    em_espera = False
                    falar(f"De volta, {saudacao()}.")
                continue

            fila_interface.put({"tipo": "estado", "valor": "ouvindo"})
            falar(f"Sim, {saudacao()}.")
            fila_interface.put({"tipo": "mensagem", "quem": "jarvis", "texto": f"Sim, {saudacao()}?"})
            comando = ouvir_comando()

            if comando is None:
                fila_interface.put({"tipo": "estado", "valor": "falando"})
                falar("Não compreendi, poderia repetir?")
                continue

            fila_interface.put({"tipo": "mensagem", "quem": "voce", "texto": comando})

            if any(palavra in comando for palavra in COMANDOS_DESLIGAR):
                fila_interface.put({"tipo": "estado", "valor": "falando"})
                falar(f"Até logo, {saudacao()}. Encerrando sistemas.")
                sys.exit(0)

            if any(palavra in comando for palavra in COMANDOS_PAUSAR):
                em_espera = True
                fila_interface.put({"tipo": "estado", "valor": "falando"})
                falar("Entendido. Aguardando seu comando para retomar.")
                continue

            if any(palavra in comando for palavra in COMANDOS_PARAR):
                fila_interface.put({"tipo": "estado", "valor": "falando"})
                falar("Tudo bem, estou aqui")
                continue

            fila_interface.put({"tipo": "estado", "valor": "processando"})
            resultado = processar(comando)

            if resultado["tipo"] == "acao":
                mensagem = executar_acao(resultado["funcao"], resultado["argumentos"])
                if mensagem:
                    fila_interface.put({"tipo": "estado", "valor": "falando"})
                    fila_interface.put({"tipo": "mensagem", "quem": "jarvis", "texto": mensagem})
                    falar(mensagem)
            else:
                resposta = resultado["conteudo"]
                if resposta_longa(resposta):
                    caminho = salvar_em_arquivo(resposta)
                    aviso = f"Preparei uma resposta mais detalhada, {saudacao()}. Salvei em {caminho}"
                    fila_interface.put({"tipo": "estado", "valor": "falando"})
                    fila_interface.put({"tipo": "mensagem", "quem": "jarvis", "texto": aviso})
                    falar(aviso)
                else:
                    fila_interface.put({"tipo": "estado", "valor": "falando"})
                    fila_interface.put({"tipo": "mensagem", "quem": "jarvis", "texto": resposta})
                    falar(resposta)

        except SystemExit:
            raise
        except Exception as erro:
            print(f"[ERRO INESPERADO] {erro}")
            try:
                fila_interface.put("falando")
                falar("Desculpe, algo deu errado. Pode repetir?")
            except:
                pass

        finally:
            pausar_escuta.clear()
            fila_interface.put({"tipo": "estado", "valor": "aguardando"})

if __name__ == "__main__":
    thread_palmas = threading.Thread(target=escutar_palmas, args=(fila_ativacao,), daemon=True)
    thread_voz = threading.Thread(target=escutar_wake_word, args=(fila_ativacao,), daemon=True)
    thread_processamento = threading.Thread(target=processar_comando, daemon=True)

    thread_palmas.start()
    thread_voz.start()
    thread_processamento.start()

    bandeja = BandejaJarvis(
        callback_mostrar=mostrar_painel,
        callback_ocultar=ocultar_painel,
        callback_pausar=alternar_pausa,
        callback_sair=sair_do_programa
    )
    bandeja.rodar_em_thread()

    threading.Thread(
        target=lambda: falar(f"Olá, {saudacao()}, no que posso ajudar?"),
        daemon=True
    ).start()

    janela_jarvis = JanelaJarvis(fila_interface)
    janela_jarvis.rodar()