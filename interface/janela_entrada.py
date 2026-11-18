
import tkinter as tk
from tkinter import ttk, messagebox

from interface.menu_direcao import criar_menu_direcao


def criar_interface(janela):

    janela.title("LinguaViva")
    janela.geometry("500x600")
    janela.resizable(False, False)

    frame = ttk.LabelFrame(
        janela,
        text="LinguaViva — Centro de Línguas",
        padding=25
    )
    frame.pack(
        padx=30,
        pady=80,
        fill="both",
        expand=True
    )

    titulo = ttk.Label(
        frame,
        text="Bem-vindo!",
        font=("Arial", 20, "bold")
    )
    titulo.pack(pady=30)

    perfil = ttk.Combobox(
        frame,
        values=[
            "Secretaria",
            "Professor",
            "Direção",
            "Encarregado"
        ],
        state="readonly",
        width=25
    )
    perfil.pack(pady=10)

    perfil.set("Selecione um perfil")

    def entrar():

        escolha = perfil.get()

        if escolha not in [
            "Secretaria",
            "Professor",
            "Direção",
            "Encarregado"
        ]:
            messagebox.showwarning(
                "Aviso",
                "Selecione um perfil!"
            )
            return

        if escolha == "Secretaria":
            from interface.menu_secretaria_gui import abrir_menu_secretaria

            for widget in janela.winfo_children():
                widget.destroy()
            abrir_menu_secretaria(janela)

        elif escolha == "Professor":
            print("Menu Professor")

        elif escolha == "Direção":
            from interface.menu_direcao import criar_menu_direcao

            criar_menu_direcao(janela)

        elif escolha == "Encarregado":
            print("Menu Encarregado")

    btn_entrar = ttk.Button(
        frame,
        text="Entrar",
        command=entrar
    )
    btn_entrar.pack(pady=30)
