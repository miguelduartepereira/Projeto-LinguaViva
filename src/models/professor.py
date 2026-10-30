from __future__ import annotations


class Professor:
    def __init__(self, id: int, nome: str, telefone: str = "", email: str = "",
                 custoHora: float = 0.0, ativo: bool = True):
        self._id = id
        self._nome = nome
        self._telefone = telefone
        self._email = email
        self._custoHora = custoHora
        self._ativo = ativo
        self._turmas: list[Turma] = []
        self._aulas: list[Aula] = []
        self._idiomas: list[Idioma] = []

    def getTurmasAtivas(self) -> list[Turma]:
        return [t for t in self._turmas if t._ativa]

    def podeDesativar(self) -> bool:
        return len(self.getTurmasAtivas()) == 0
