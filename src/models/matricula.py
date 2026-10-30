from __future__ import annotations

from datetime import date


class Matricula:
    def __init__(self, id: int, dataMatricula: date, valorPropina: float,
                 estado: str = "ativa", notaFinal: float | None = None):
        self._id = id
        self._dataMatricula = dataMatricula
        self._valorPropina = valorPropina
        self._estado = estado
        self._notaFinal = notaFinal
        self._aluno: Aluno | None = None
        self._turma: Turma | None = None
        self._avaliacoes: list[Avaliacao] = []
        self._presencas: list[Presenca] = []
        self._certificado: Certificado | None = None

    def calcularAssiduidade(self) -> float:
        total = len(self._presencas)
        if total == 0:
            return 0.0
        presentes = sum(1 for p in self._presencas if p._estado in ("P", "J"))
        return presentes / total * 100

    def calcularNotaFinal(self) -> float:
        nivel = self._turma._nivel if self._turma else None
        if nivel is None:
            return 0.0
        pesos = {
            "oral": nivel._pondOral,
            "escrito": nivel._pondEscrito,
            "projeto": nivel._pondProjeto,
        }
        nota = 0.0
        for avaliacao in self._avaliacoes:
            nota += avaliacao._nota * pesos.get(avaliacao._tipo, 0.0)
        return nota

    def estaAprovado(self) -> bool:
        return self.calcularAssiduidade() >= 75 and (self._notaFinal or 0.0) >= 10

    def cancelar(self) -> None:
        self._estado = "cancelada"
