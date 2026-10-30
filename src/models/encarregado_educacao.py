from __future__ import annotations

class EncarregadoEducacao:
    def __init__(self, id: int, nome: str, nif: str,
                 telefone: str = "", email: str = "", parentesco: str = ""):
        self._id = id
        self._nome = nome
        self._nif = nif
        self._telefone = telefone
        self._email = email
        self._parentesco = parentesco
        self._alunos: list[Aluno] = []

    def registarConsentimento(self) -> None:
        for aluno in self._alunos:
            aluno._consentimentoRGPD = True