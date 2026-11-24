import tkinter as tk
from tkinter import messagebox

from repositories.utilizador_repository import UtilizadorRepository
from services.auth_service import AuthService


_auth_service = AuthService(UtilizadorRepository())


def criar_interface(janela):
    janela.title("LinguaViva - Acesso")
    janela.geometry("400x300")
    janela.resizable(False, False)

    tk.Label(janela, text="Utilizador:").pack(pady=(30, 2))
    entry_user = tk.Entry(janela, width=30)
    entry_user.pack()

    tk.Label(janela, text="Password:").pack(pady=(10, 2))
    entry_pass = tk.Entry(janela, width=30, show="*")
    entry_pass.pack()

    def entrar():
        login = entry_user.get().strip()
        senha = entry_pass.get()
        if not login or not senha:
            messagebox.showwarning("LinguaViva", "Preencha todos os campos.")
            return

        try:
            utilizador = _auth_service.autenticar(login, senha)
            token = _auth_service.criar_token(utilizador)
            _abrir_menu_perfil(janela, utilizador._perfil, token)
        except ValueError as erro:
            messagebox.showerror("LinguaViva", str(erro))
            entry_pass.delete(0, tk.END)

    tk.Button(janela, text="Entrar", command=entrar, width=15).pack(pady=20)
    entry_user.focus_set()


def _abrir_menu_perfil(janela, perfil, token):
    for widget in janela.winfo_children():
        widget.destroy()

    # The token is retained on the window until the later RBAC work passes it
    # to each protected service operation.
    janela.token_sessao = token
    perfil_normalizado = perfil.lower().replace("ç", "c").replace("ã", "a")

    if perfil_normalizado == "secretaria":
        from interface.menu_secretaria_gui import abrir_menu_secretaria
        abrir_menu_secretaria(janela)
    elif perfil_normalizado == "professor":
        from interface.menu_professor import MenuProfessorGUI
        MenuProfessorGUI(janela)
    elif perfil_normalizado == "direcao":
        from interface.menu_direcao import criar_menu_direcao
        criar_menu_direcao(janela)
    else:
        messagebox.showerror("LinguaViva", "Perfil de utilizador inválido.")
