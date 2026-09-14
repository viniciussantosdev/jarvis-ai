import speech_recognition as sr

def ouvir_comando():
    reconhecedor = sr.Recognizer()
    reconhecedor.pause_threshold = 1.5
    reconhecedor.energy_threshold = 300
    reconhecedor.dynamic_energy_threshold = True
    microfone = sr.Microphone()

    with microfone as source:
        print("Pode falar, estou ouvindo")

        try:
            audio = reconhecedor.listen(source, timeout=6, phrase_time_limit=15)
            texto = reconhecedor.recognize_google(audio, language="pt-BR")
            texto = texto.lower()
            print(f"Comando ouvido: {texto}")
            return texto
        
        except sr.WaitTimeoutError:
            print("Não ouvi nada a tempo.")
            return None
        except sr.UnknownValueError:
            print("Não consegui entender o que foi dito, poderia repetir?")
        except sr.RequestError:
            print("Erro de conexão com o serviço de reconhecimento")
            return None

if __name__ == "__main__":
    comando = ouvir_comando()
    print(f"Resultado retornado: {comando}")