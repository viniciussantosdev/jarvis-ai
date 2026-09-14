import asyncio
import edge_tts
import os
from  playsound import playsound

VOZ = "pt-BR-AntonioNeural"
PITCH = "-20Hz"
ARQUIVO_TEMP = "resposta.mp3"

async def gerar_audio(texto):
    comunicador = edge_tts.Communicate(texto, VOZ, pitch=PITCH)
    await comunicador.save(ARQUIVO_TEMP)

def falar(texto):
    print(f"Jarvis: {texto}")
    asyncio.run(gerar_audio(texto))
    playsound(ARQUIVO_TEMP)
    os.remove(ARQUIVO_TEMP)

if __name__ == "__main__":
    falar("Olá senhor Vinicius, o seu relatório esta 78% pronto, gostaria de analisar?")