from __future__ import annotations


class Idioma:
    def __init__(self, id: int, nome: str, codigo: str):
        self._id = id
        self._nome = nome
        self._codigo = codigo
        self._turmas: list[Turma] = []
        self._professores: list[Professor] = []

    def getTurmas(self) -> list[Turma]:
        return list(self._turmas)
