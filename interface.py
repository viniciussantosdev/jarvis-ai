import tkinter as tk
import math
import random
import queue

LARGURA = 320
ALTURA = 420
COR_FUNDO = "#0a0e14"
COR_ORBE = "#5ad1ff"
COR_ORBE_CLARO = "#b6ecff"

CORES_STATUS = {
    "aguardando": "#5ad1ff",
    "ouvindo": "#6dffb0",
    "processando": "#ffcc66",
    "falando": "#ff8ac2"
}

TEXTOS_STATUS = {
    "aguardando": "AGUARDANDO",
    "ouvindo": "OUVINDO",
    "processando": "PROCESSANDO",
    "falando": "FALANDO"
}

class JanelaJarvis:
    def __init__(self, fila_eventos):
        self.fila_eventos = fila_eventos
        self.estado_atual = "aguardando"

        self.janela = tk.Tk()
        self.janela.title("Jarvis")
        self.janela.configure(bg=COR_FUNDO)
        self.janela.geometry(f"{LARGURA}x{ALTURA}")
        self.janela.attributes("-topmost", True)

        self.canvas = tk.Canvas(
            self.janela, width=LARGURA, height=200,
            bg=COR_FUNDO, highlightthickness=0
        )
        self.canvas.pack()

        self.label_status = tk.Label(
            self.janela, text=TEXTOS_STATUS["aguardando"],
            bg=COR_FUNDO, fg=COR_ORBE_CLARO,
            font=("Consolas", 9)
        )
        self.label_status.pack(pady=(0, 10))

        self.criar_area_transcricao()

        self.cx = LARGURA // 2
        self.cy = 100
        self.raio_base = 45
        self.particulas = []

        for _ in range(60):
            angulo = random.uniform(0, math.pi * 2)
            distancia = self.raio_base * math.sqrt(random.uniform(0, 1))
            self.particulas.append({
                "angulo": angulo,
                "distancia": distancia,
                "velocidade": random.uniform(0.003, 0.008),
                "tamanho": random.uniform(1, 2.5)
            })

        self.pulso = 0
        self.checar_fila()
        self.animar()

    def criar_area_transcricao(self):
        frame = tk.Frame(self.janela, bg=COR_FUNDO)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.texto_chat = tk.Text(
            frame,
            bg="#10151d",
            fg="#d8dee6",
            font=("Consolas", 9),
            wrap="word",
            state="disabled",
            yscrollcommand=scrollbar.set,
            relief="flat",
            padx=8, pady=8
        )
        self.texto_chat.pack(fill="both", expand=True)
        scrollbar.config(command=self.texto_chat.yview)

        self.texto_chat.tag_config("voce", foreground="#7a8494")
        self.texto_chat.tag_config("jarvis", foreground="#6dffb0")
        self.texto_chat.tag_config("corpo", foreground="#d8dee6")

    def adicionar_mensagem(self, quem, texto):
        self.texto_chat.config(state="normal")

        if quem == "voce":
            self.texto_chat.insert("end", "Eu: ", "voce")
        else:
            self.texto_chat.insert("end", "J.A.R.V.I.S: ", "jarvis")

        self.texto_chat.insert("end", f"{texto}\n\n", "corpo")
        self.texto_chat.config(state="disabled")
        self.texto_chat.see("end")

    def checar_fila(self):
        try:
            while True:
                evento = self.fila_eventos.get_nowait()

                if evento["tipo"] == "estado":
                    self.mudar_estado(evento["valor"])
                elif evento["tipo"] == "mensagem":
                    self.adicionar_mensagem(evento["quem"], evento["texto"])

        except queue.Empty:
            pass

        self.janela.after(100, self.checar_fila)

    def mudar_estado(self, novo_estado):
        if novo_estado in CORES_STATUS:
            self.estado_atual = novo_estado
            self.label_status.config(
                text=TEXTOS_STATUS[novo_estado],
                fg=CORES_STATUS[novo_estado]
            )

    def animar(self):
        self.canvas.delete("all")
        self.pulso += 0.015

        velocidade_pulso = 4 if self.estado_atual == "aguardando" else 8
        raio_atual = self.raio_base + math.sin(self.pulso) * velocidade_pulso

        cor_atual = CORES_STATUS[self.estado_atual]

        for p in self.particulas:
            p["angulo"] += p["velocidade"]
            x = self.cx + math.cos(p["angulo"]) * p["distancia"]
            y = self.cy + math.sin(p["angulo"]) * p["distancia"] * 0.6

            self.canvas.create_oval(
                x - p["tamanho"], y - p["tamanho"],
                x + p["tamanho"], y + p["tamanho"],
                fill=COR_ORBE_CLARO, outline=""
            )

        self.canvas.create_oval(
            self.cx - raio_atual, self.cy - raio_atual,
            self.cx + raio_atual, self.cy + raio_atual,
            outline=cor_atual, width=1
        )

        self.janela.after(30, self.animar)

    def rodar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    fila_teste = queue.Queue()
    app = JanelaJarvis(fila_teste)
    app.rodar()