from __future__ import annotations

from models.aula import Aula
from models.presenca import Presenca
from repositories.aula_repository import AulaRepository


class AulaService:
    ESTADOS_PRESENCA = ("P", "A", "J")

    def __init__(self):
        self._repo = AulaRepository()

    def registar(self, aula: Aula) -> int:
        if aula._turma is None:
            raise ValueError("A aula tem de pertencer a uma turma.")
        if aula._professor is None:
            raise ValueError("A aula tem de ter um professor.")
        if aula._data is None:
            raise ValueError("A aula tem de ter data.")
        return self._repo.inserir(aula)

    def registar_presencas(self, aula_id: int, presencas: list[Presenca]) -> None:
        if self._repo.obter_por_id(aula_id) is None:
            raise ValueError("Aula não encontrada.")
        for presenca in presencas:
            if presenca._estado not in self.ESTADOS_PRESENCA:
                raise ValueError("Estado de presença inválido (P/A/J).")
            if presenca._matricula is None:
                raise ValueError("Cada presença tem de estar ligada a uma matrícula.")
        self._repo.inserir_presencas(aula_id, presencas)

    def obter(self, aula_id: int) -> Aula | None:
        return self._repo.obter_por_id(aula_id)

    def listar_por_turma(self, turma_id: int) -> list[Aula]:
        return self._repo.listar_por_turma(turma_id)

    def listar_presencas_por_aula(self, aula_id: int) -> list[Presenca]:
        return self._repo.listar_presencas_por_aula(aula_id)
