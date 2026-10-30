from __future__ import annotations

from datetime import date

from models.aluno import Aluno
from models.matricula import Matricula
from repositories.aluno_repository import AlunoRepository
from repositories.matricula_repository import MatriculaRepository


class AlunoService:
    IDADE_MAIORIDADE = 18

    def __init__(self):
        self._repo = AlunoRepository()
        self._matriculas = MatriculaRepository()

    def registar(self, aluno: Aluno) -> int:
        self._validar(aluno)
        return self._repo.inserir(aluno)

    def arquivar(self, aluno_id: int) -> None:
        if self._repo.obter_por_id(aluno_id) is None:
            raise ValueError("Aluno não encontrado.")
        self._repo.arquivar(aluno_id)

    def obter(self, aluno_id: int) -> Aluno | None:
        return self._repo.obter_por_id(aluno_id)

    def pesquisar(self, termo: str) -> list[Aluno]:
        if not termo or not termo.strip():
            return self._repo.listar_todos()
        return self._repo.pesquisar(termo.strip())

    def listar(self) -> list[Aluno]:
        return self._repo.listar_todos()

    def obter_historico(self, aluno_id: int) -> list[Matricula]:
        if self._repo.obter_por_id(aluno_id) is None:
            raise ValueError("Aluno não encontrado.")
        return self._matriculas.listar_por_aluno(aluno_id)

    def _validar(self, aluno: Aluno) -> None:
        if not aluno._nome or not aluno._nome.strip():
            raise ValueError("O nome do aluno é obrigatório.")
        if not self._nif_valido(aluno._nif):
            raise ValueError("NIF inválido. Deve ter 9 dígitos.")
        if aluno._dataNasc is None:
            raise ValueError("A data de nascimento é obrigatória.")
        if aluno._email and not self._email_valido(aluno._email):
            raise ValueError("Email inválido.")
        if self._e_menor(aluno):
            if aluno._id_encarregado is None:
                raise ValueError("Alunos menores precisam de encarregado de educação (RGPD).")
            if not aluno._consentimentoRGPD:
                raise ValueError("Alunos menores precisam de consentimento RGPD explicito.")

    def _nif_valido(self, nif: str) -> bool:
        return nif is not None and nif.isdigit() and len(nif) == 9

    def _email_valido(self, email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]

    def _e_menor(self, aluno: Aluno) -> bool:
        hoje = date.today()
        idade = hoje.year - aluno._dataNasc.year - (
            (hoje.month, hoje.day) < (aluno._dataNasc.month, aluno._dataNasc.day)
        )
        return idade < self.IDADE_MAIORIDADE
