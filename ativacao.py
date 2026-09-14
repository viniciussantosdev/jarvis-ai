import sounddevice as sd
import numpy as np
import time
import speech_recognition as sr
import threading

LIMITE_VOLUME = 5.0
LIMITE_SILENCIO = 2.0
JANELA_TEMPO = 1.5
DEBOUNCE = 0.3
ATRASO_CONFIRMACAO = 0.5

ultima_palma = 0 
ultimo_pico_bruto = 0
pausar_escuta = threading.Event()
contador_palmas = 0
volume_anterior = 0
temporizador_confirmacao = None

fila_global = None
def confirmar_ativacao():
    global contador_palmas
    fila_global.put("ativado")
    contador_palmas = 0

def callback(indata, frames, time_info, status):
    global ultima_palma, ultimo_pico_bruto, contador_palmas, volume_anterior, temporizador_confirmacao

    volume = np.linalg.norm(indata) * 10
    agora = time.time()

    pico_e_repentino = volume > LIMITE_VOLUME and volume_anterior < LIMITE_SILENCIO
    tempo_liberado = (agora - ultimo_pico_bruto) > DEBOUNCE
    
    if pico_e_repentino and tempo_liberado:
        ultimo_pico_bruto = agora

        if agora- ultima_palma < JANELA_TEMPO:
            contador_palmas += 1
        else: 
            contador_palmas = 1
        ultima_palma = agora

        if contador_palmas == 2:
            if temporizador_confirmacao is not None:
                temporizador_confirmacao.cancel()
            temporizador_confirmacao = threading.Timer(ATRASO_CONFIRMACAO, confirmar_ativacao)
            temporizador_confirmacao.start()

        elif contador_palmas > 2:
            if temporizador_confirmacao is not None:
                temporizador_confirmacao.cancel()
            print("Mais de duas palmas detectadas")
            contador_palmas=0
    volume_anterior = volume

def escutar_palmas(fila):
    global fila_global
    fila_global = fila

    with sd.InputStream(callback=callback):
        print("Escutando por duas palmas")
        while True:
            time.sleep(0.1)

def escutar_wake_word(fila):
    reconhecedor = sr.Recognizer()
    reconhecedor.pause_threshold = 1.2
    reconhecedor.energy_threshold = 300
    reconhecedor.dynamic_energy_adjustment_damping = True
    microfone = sr.Microphone()

    with microfone as source:
        reconhecedor.adjust_for_ambient_noise(source, duration=1)

    print("Escutando por Jarvis..")

    while True:
        if pausar_escuta.is_set():
            time.sleep(0.2)
            continue
        with microfone as source:
            try:
                audio = reconhecedor.listen(source, timeout=5, phrase_time_limit=5)
                texto = reconhecedor.recognize_google(audio,language="pt-BR")
                texto = texto.lower()
                print(f"Ouvi: {texto}")

                if "jarvis" in texto:
                    fila.put("ativado")

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Erro de conexão com o serviço de reconhecimento")

def iniciar_ativacao():
    thread_palmas = threading.Thread(target=escutar_palmas, daemon=True)
    thread_voz = threading.Thread(target=escutar_wake_word,daemon=True)

    thread_palmas.start()
    thread_voz.start()

    thread_palmas.join()
    thread_voz.join() 

if __name__ == "__main__":
    iniciar_ativacao()