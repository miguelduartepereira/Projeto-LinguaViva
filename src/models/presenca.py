from __future__ import annotations


class Presenca:
    def __init__(self, id: int, estado: str = "A"):
        self._id = id
        self._estado = estado
        self._aula: Aula | None = None
        self._matricula: Matricula | None = None

    def marcar(self, estado: str) -> None:
        if estado in ("P", "A", "J"):
            self._estado = estado
