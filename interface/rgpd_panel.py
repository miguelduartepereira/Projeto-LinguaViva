import tkinter as tk
from tkinter import ttk

class RGPDPanel(ttk.LabelFrame):
    def __init__(self, parent, callback_confirmacao=None):
        super().__init__(parent, text="Aviso RGPD")
        self.callback_confirmacao = callback_confirmacao

        texto_aviso = (
            "O centro de línguas LinguaViva gere dados pessoais de menores de idade.\n"
            "O acesso a esta informação está sujeito ao Regulamento Geral de Proteção de Dados (RGPD)."
        )
        
        self.label_aviso = ttk.Label(self, text=texto_aviso, wraplength=350, justify="left")
        self.label_aviso.pack(padx=10, pady=10)

        self.var_confirmacao = tk.BooleanVar(value=False)
        self.chk_confirmar = ttk.Checkbutton(
            self, 
            text="Confirmo que tenho autorização do encarregado de educação", 
            variable=self.var_confirmacao,
            command=self.ao_alterar_estado
        )
        self.chk_confirmar.pack(padx=10, pady=5, anchor="w")

    def ao_alterar_estado(self):
        if self.callback_confirmacao:
            self.callback_confirmacao(self.var_confirmacao.get())
