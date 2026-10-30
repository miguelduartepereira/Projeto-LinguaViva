from __future__ import annotations

from datetime import date


class Aula:
    def __init__(self, id: int, data: date, sumario: str):
        self._id = id
        self._data = data
        self._sumario = sumario
        self._turma: Turma | None = None
        self._professor: Professor | None = None
        self._presencas: list[Presenca] = []

    def eSubstituicao(self) -> bool:
        if self._turma is None or self._professor is None:
            return False
        return self._professor is not self._turma._professor
