from __future__ import annotations

from datetime import date

from models.avaliacao import Avaliacao
from models.certificado import Certificado
from models.matricula import Matricula
from repositories.aula_repository import AulaRepository
from repositories.matricula_repository import MatriculaRepository
from repositories.turma_repository import TurmaRepository


class MatriculaService:
    TIPOS_AVALIACAO = ("oral", "escrito", "projeto")
    ASSIDUIDADE_MINIMA = 75
    NOTA_MINIMA = 10

    def __init__(self):
        self._repo = MatriculaRepository()
        self._turmas = TurmaRepository()
        self._aulas = AulaRepository()

    def matricular(self, matricula: Matricula) -> int:
        if matricula._aluno is None:
            raise ValueError("A matrícula tem de ter um aluno.")
        if matricula._turma is None:
            raise ValueError("A matrícula tem de ter uma turma.")
        turma = matricula._turma
        ativas = self._turmas.contar_matriculas_ativas(turma._id)
        if ativas >= turma._maxAlunos:
            raise ValueError("A turma não tem vagas disponíveis.")
        matricula._estado = "ativa"
        return self._repo.inserir(matricula)

    def cancelar(self, matricula_id: int) -> None:
        if self._repo.obter_por_id(matricula_id) is None:
            raise ValueError("Matrícula não encontrada.")
        self._repo.cancelar(matricula_id)

    def registar_avaliacao(self, matricula_id: int, avaliacao: Avaliacao) -> int:
        if self._repo.obter_por_id(matricula_id) is None:
            raise ValueError("Matrícula não encontrada.")
        if avaliacao._tipo not in self.TIPOS_AVALIACAO:
            raise ValueError("Tipo de avaliação inválido (oral/escrito/projeto).")
        if not avaliacao.validarNota():
            raise ValueError("A nota tem de estar entre 0 e 20.")
        return self._repo.inserir_avaliacao(matricula_id, avaliacao)

    def listar_avaliacoes(self, matricula_id: int) -> list[Avaliacao]:
        return self._repo.listar_avaliacoes(matricula_id)

    def calcular_nota_final(self, matricula: Matricula) -> float:
        matricula._avaliacoes = self._repo.listar_avaliacoes(matricula._id)
        nota = round(matricula.calcularNotaFinal(), 2)
        matricula._notaFinal = nota
        self._repo.atualizar_nota_final(matricula._id, nota)
        return nota

    def calcular_assiduidade(self, matricula: Matricula) -> float:
        matricula._presencas = self._aulas.listar_presencas_por_matricula(matricula._id)
        return matricula.calcularAssiduidade()

    def emitir_certificado(self, matricula: Matricula) -> Certificado:
        if self._repo.obter_certificado(matricula._id) is not None:
            raise ValueError("Já existe certificado para esta matrícula.")
        atual = self._repo.obter_por_id(matricula._id)
        if atual is None:
            raise ValueError("Matrícula não encontrada.")
        if atual._notaFinal is None:
            raise ValueError("A nota final ainda não foi calculada.")
        assiduidade = self.calcular_assiduidade(matricula)
        if assiduidade < self.ASSIDUIDADE_MINIMA or atual._notaFinal < self.NOTA_MINIMA:
            raise ValueError("Certificado apenas para assiduidade >= 75% e nota final >= 10.")
        certificado = Certificado(0)
        certificado._matricula = matricula
        certificado._dataEmissao = date.today()
        certificado._numero = f"TMP-{matricula._id}"
        certificado._id = self._repo.inserir_certificado(matricula._id, certificado)
        certificado.gerarNumero()
        certificado._ficheiroPdf = f"certificado_{certificado._numero}.pdf"
        self._repo.atualizar_certificado(
            certificado._id, certificado._numero, certificado._ficheiroPdf
        )
        return certificado
