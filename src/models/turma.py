from __future__ import annotations


class Turma:
    def __init__(self, id: int, horario: str, sala: str, maxAlunos: int,
                 semestre: int, ano: int, ativa: bool = True):
        self._id = id
        self._horario = horario
        self._sala = sala
        self._maxAlunos = maxAlunos
        self._semestre = semestre
        self._ano = ano
        self._ativa = ativa
        self._idioma: Idioma | None = None
        self._nivel: Nivel | None = None
        self._professor: Professor | None = None
        self._matriculas: list[Matricula] = []
        self._aulas: list[Aula] = []

    def vagasDisponiveis(self) -> int:
        ocupadas = sum(1 for m in self._matriculas if m._estado == "ativa")
        return self._maxAlunos - ocupadas

    def temVagas(self) -> bool:
        return self.vagasDisponiveis() > 0
