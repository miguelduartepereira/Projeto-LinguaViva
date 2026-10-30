from __future__ import annotations


class Nivel:
    def __init__(self, id: int, codigo: str, descricao: str,
                 pondOral: float, pondEscrito: float, pondProjeto: float):
        self._id = id
        self._codigo = codigo
        self._descricao = descricao
        self._pondOral = pondOral
        self._pondEscrito = pondEscrito
        self._pondProjeto = pondProjeto
        self._turmas: list[Turma] = []

    def validarPonderacoes(self) -> bool:
        return abs((self._pondOral + self._pondEscrito + self._pondProjeto) - 1.0) < 0.001
