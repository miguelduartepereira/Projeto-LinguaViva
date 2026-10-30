from __future__ import annotations

from datetime import date


class Certificado:
    def __init__(self, id: int, numero: str = "", dataEmissao: date | None = None,
                 ficheiroPdf: str = ""):
        self._id = id
        self._numero = numero
        self._dataEmissao = dataEmissao
        self._ficheiroPdf = ficheiroPdf
        self._matricula: Matricula | None = None

    def gerarNumero(self) -> str:
        ano = (self._dataEmissao or date.today()).year
        idioma = "XXX"
        nivel = "XX"
        if self._matricula and self._matricula._turma:
            turma = self._matricula._turma
            if turma._idioma:
                idioma = turma._idioma._codigo
            if turma._nivel:
                nivel = turma._nivel._codigo
        self._numero = f"{ano}-{idioma}-{nivel}-{self._id:04d}"
        return self._numero

    def gerarPDF(self) -> None:
        if not self._numero:
            self.gerarNumero()
        self._dataEmissao = self._dataEmissao or date.today()
        self._ficheiroPdf = f"certificado_{self._numero}.pdf"
