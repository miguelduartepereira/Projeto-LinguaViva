from __future__ import annotations

from models.idioma import Idioma
from repositories.idioma_repository import IdiomaRepository


class IdiomaService:
    def __init__(self):
        self._repo = IdiomaRepository()

    def registar(self, idioma: Idioma) -> int:
        if not idioma._nome or not idioma._nome.strip():
            raise ValueError("O nome do idioma é obrigatório.")
        if not idioma._codigo or not idioma._codigo.strip():
            raise ValueError("O código do idioma é obrigatório.")
        if self._repo.obter_por_codigo(idioma._codigo) is not None:
            raise ValueError("Já existe um idioma com esse código.")
        return self._repo.inserir(idioma)

    def obter(self, idioma_id: int) -> Idioma | None:
        return self._repo.obter_por_id(idioma_id)

    def obter_por_codigo(self, codigo: str) -> Idioma | None:
        return self._repo.obter_por_codigo(codigo)

    def listar(self) -> list[Idioma]:
        return self._repo.listar_todos()
