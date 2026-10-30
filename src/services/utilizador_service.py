from __future__ import annotations

import hashlib

from models.utilizador import Utilizador
from repositories.utilizador_repository import UtilizadorRepository


class UtilizadorService:
    PERFIS_VALIDOS = ("Secretaria", "Professor", "Direcao")

    def __init__(self):
        self._repo = UtilizadorRepository()

    def registar(self, username: str, password: str, perfil: str) -> int:
        if not username or not username.strip():
            raise ValueError("O username é obrigatório.")
        if not password:
            raise ValueError("A password é obrigatória.")
        if perfil not in self.PERFIS_VALIDOS:
            raise ValueError("Perfil inválido (Secretaria/Professor/Direcao).")
        if self._repo.obter_por_username(username) is not None:
            raise ValueError("Já existe um utilizador com esse username.")
        utilizador = Utilizador(0, username, self._hash(password), perfil)
        return self._repo.inserir(utilizador)

    def autenticar(self, username: str, password: str) -> Utilizador | None:
        utilizador = self._repo.obter_por_username(username)
        if utilizador is None or not utilizador._ativo:
            return None
        if utilizador._passwordHash != self._hash(password):
            return None
        return utilizador

    def tem_permissao(self, utilizador: Utilizador, acao: str) -> bool:
        return utilizador.temPermissao(acao)
