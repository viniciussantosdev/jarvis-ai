import pystray
from PIL import Image, ImageDraw
import threading

def criar_icone():
    imagem = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    desenho = ImageDraw.Draw(imagem)
    desenho.ellipse((8, 8, 56, 56), fill=(90, 209, 255, 255))
    desenho.ellipse((20, 20, 44, 44), fill=(182, 236, 255, 255))
    return imagem

class BandejaJarvis:
    def __init__(self, callback_mostrar, callback_ocultar, callback_pausar, callback_sair):
        self.callback_mostrar = callback_mostrar
        self.callback_ocultar = callback_ocultar
        self.callback_pausar = callback_pausar
        self.callback_sair = callback_sair

        menu = pystray.Menu(
            pystray.MenuItem("Mostrar painel", self._mostrar),
            pystray.MenuItem("Ocultar painel", self._ocultar),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Pausar Jarvis", self._pausar),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Sair", self._sair)
        )

        self.icone = pystray.Icon("jarvis", criar_icone(), "Jarvis", menu)

    def _mostrar(self, icon, item):
        self.callback_mostrar()

    def _ocultar(self, icon, item):
        self.callback_ocultar()

    def _pausar(self, icon, item):
        self.callback_pausar()

    def _sair(self, icon, item):
        self.callback_sair()
        self.icone.stop()

    def rodar_em_thread(self):
        thread = threading.Thread(target=self.icone.run, daemon=True)
        thread.start()