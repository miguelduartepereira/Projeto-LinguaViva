from __future__ import annotations

from datetime import date


class Avaliacao:
    def __init__(self, id: int, tipo: str, nota: float, data: date):
        self._id = id
        self._tipo = tipo
        self._nota = nota
        self._data = data
        self._matricula: Matricula | None = None

    def validarNota(self) -> bool:
        return 0 <= self._nota <= 20
