# criar_utilizadores.py
# Cria as contas de acesso (uma por perfil) com password guardada em bcrypt.
# Correr uma vez: python criar_utilizadores.py

import sys
from getpass import getpass

sys.path.append(".")
sys.path.append("src")

from db.connection import inicializar_bd
from services.auth_service import AuthService, PERFIS_VALIDOS

inicializar_bd()
auth = AuthService()

print("=== Criar utilizadores do LinguaViva ===")
print("Perfis:", ", ".join(PERFIS_VALIDOS))

while True:
    login = input("\nUtilizador (Enter para terminar): ").strip()
    if login == "":
        break
    perfil = input("Perfil: ").strip()
    senha = getpass("Password (mín. 8 caracteres): ")   # não aparece no ecrã
    if senha != getpass("Repetir password: "):
        print("As passwords não são iguais.")
        continue
    try:
        novo_id = auth.registar(login, senha, perfil)
        print("OK utilizador criado com id", novo_id)
    except ValueError as erro:
        print("Erro:", erro)
