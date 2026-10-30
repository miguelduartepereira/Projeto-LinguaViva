from __future__ import annotations

from models.nivel import Nivel
from repositories.nivel_repository import NivelRepository


class NivelService:
    CODIGOS_VALIDOS = ("A1", "A2", "B1", "B2", "C1", "C2")

    def __init__(self):
        self._repo = NivelRepository()

    def registar(self, nivel: Nivel) -> int:
        if nivel._codigo not in self.CODIGOS_VALIDOS:
            raise ValueError("Código de nível inválido. Use A1 a C2.")
        if self._repo.obter_por_codigo(nivel._codigo) is not None:
            raise ValueError("Já existe um nível com esse código.")
        if not nivel.validarPonderacoes():
            raise ValueError("As ponderações (oral + escrito + projeto) têm de somar 1.")
        return self._repo.inserir(nivel)

    def obter(self, nivel_id: int) -> Nivel | None:
        return self._repo.obter_por_id(nivel_id)

    def obter_por_codigo(self, codigo: str) -> Nivel | None:
        return self._repo.obter_por_codigo(codigo)

    def listar(self) -> list[Nivel]:
        return self._repo.listar_todos()
