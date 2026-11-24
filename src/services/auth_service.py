# src/services/auth_service.py
# Autenticação do LinguaViva — Lab 1 (bcrypt) e Lab 2 (JWT)
# Rui Gonçalves - Grupo 4

import os
import datetime

import bcrypt
import jwt

from models.utilizador import Utilizador
from repositories.utilizador_repository import UtilizadorRepository

# a chave secreta vem de uma variável de ambiente (nunca escrita no código em produção)
SECRET_KEY = os.environ.get("LINGUAVIVA_SECRET", "dev-secret-linguaviva-32-caracteres")
EMISSOR = "linguaviva"
HORAS_SESSAO = 8

PERFIS_VALIDOS = ("Secretaria", "Professor", "Direcao")   # como estão na tabela Utilizador


class AuthService:
    def __init__(self, repo=None):
        self._repo = repo or UtilizadorRepository()

    # ---------- Lab 1: passwords com bcrypt ----------

    def registar(self, login, senha, perfil):
        """Regista um utilizador novo (só para administradores)."""
        if not login or not login.strip():
            raise ValueError("O utilizador é obrigatório.")
        if len(senha) < 8:
            raise ValueError("A password tem de ter pelo menos 8 caracteres.")
        if perfil not in PERFIS_VALIDOS:
            raise ValueError("Perfil inválido (Secretaria, Professor ou Direcao).")
        if self._repo.obter_por_username(login.strip()) is not None:
            raise ValueError("O utilizador '" + login + "' já existe.")

        # bcrypt gera um salt aleatório e é lento de propósito (custo 12)
        hash_senha = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt(rounds=12))
        # a coluna password_hash é TEXT, por isso guardamos o hash como texto
        u = Utilizador(0, login.strip(), hash_senha.decode("utf-8"), perfil)
        return self._repo.inserir(u)

    def autenticar(self, login, senha):
        """Devolve o utilizador se o login estiver certo; senão lança ValueError."""
        u = self._repo.obter_por_username(login.strip())

        if u is None:
            # faz na mesma uma verificação para demorar o mesmo tempo
            # e não revelar se o utilizador existe ou não
            bcrypt.checkpw(b"x", bcrypt.hashpw(b"x", bcrypt.gensalt(4)))
            raise ValueError("Credenciais inválidas.")

        if not bcrypt.checkpw(senha.encode("utf-8"), u._passwordHash.encode("utf-8")):
            raise ValueError("Credenciais inválidas.")

        if not u._ativo:
            raise ValueError("Conta desativada. Fale com a Direção.")

        return u

    # ---------- Lab 2: token de sessão com JWT ----------

    def criar_token(self, utilizador):
        agora = datetime.datetime.now(datetime.timezone.utc)
        payload = {
            "sub": utilizador._username,
            "perfil": utilizador._perfil.lower(),   # "secretaria" | "professor" | "direcao"
            "iat": agora,
            "exp": agora + datetime.timedelta(hours=HORAS_SESSAO),
            "iss": EMISSOR,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def validar_token(token):
        """Devolve os dados do token ou lança PermissionError se for inválido/expirado.
        É staticmethod para poder ser chamado sem criar um AuthService (o rbac.py usa assim)."""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"], issuer=EMISSOR)
        except jwt.ExpiredSignatureError:
            raise PermissionError("Sessão expirada. Faça login novamente.")
        except jwt.InvalidTokenError:
            raise PermissionError("Token inválido.")

    def perfil_do_token(self, token):
        return self.validar_token(token)["perfil"]
