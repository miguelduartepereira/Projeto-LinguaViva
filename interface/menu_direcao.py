
import tkinter as tk
from tkinter import ttk, messagebox

from interface.professores.gerir_professores import criar_janela_professores


def criar_menu_direcao(janela):

    for widget in janela.winfo_children():
        widget.destroy()

    janela.title("LinguaViva - Direção")
    janela.geometry("500x600")
    janela.resizable(False, False)

    frame = ttk.LabelFrame(
        janela,
        text="Menu — Direção",
        padding=25
    )
    frame.pack(
        padx=30,
        pady=50,
        fill="both",
        expand=True
    )

    titulo = ttk.Label(
        frame,
        text="Área de Gestão",
        font=("Arial", 20, "bold")
    )
    titulo.pack(pady=25)

    def gerir_professores():
        from interface.professores.gerir_professores import (
            criar_janela_professores
        )

        criar_janela_professores(janela)

    def gerir_turmas():
        from interface.turmas.gerir_turmas import criar_janela_turmas
        criar_janela_turmas(janela)
    

    def relatorios():
        from interface.relatorios.gerir_relatorios import (
            criar_janela_relatorios
        )

        criar_janela_relatorios(janela)

    def sair():
        janela.destroy()

    botoes = [
        ("Gerir Professores", gerir_professores),
        ("Gerir Turmas", gerir_turmas),
        ("Relatórios", relatorios),
        ("Sair", sair)
    ]

    for texto, comando in botoes:
        botao = ttk.Button(
            frame,
            text=texto,
            command=comando,
            width=30
        )

        botao.pack(pady=10, ipady=5)
