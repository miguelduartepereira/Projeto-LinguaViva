from __future__ import annotations

from models.turma import Turma
from repositories.turma_repository import TurmaRepository


class TurmaService:
    MIN_ALUNOS = 6
    MAX_ALUNOS = 12

    def __init__(self):
        self._repo = TurmaRepository()

    def criar(self, turma: Turma) -> int:
        if turma._idioma is None:
            raise ValueError("A turma tem de ter um idioma.")
        if turma._nivel is None:
            raise ValueError("A turma tem de ter um nível.")
        if turma._professor is None:
            raise ValueError("A turma tem de ter um professor.")
        if turma._semestre not in (1, 2):
            raise ValueError("O semestre tem de ser 1 ou 2.")
        if not (self.MIN_ALUNOS <= turma._maxAlunos <= self.MAX_ALUNOS):
            raise ValueError("O número máximo de alunos tem de estar entre 6 e 12.")
        return self._repo.inserir(turma)

    def obter(self, turma_id: int) -> Turma | None:
        return self._repo.obter_por_id(turma_id)

    def listar(self) -> list[Turma]:
        return self._repo.listar_todas()

    def listar_com_inscritos(self) -> list[dict]:
        return self._repo.listar_com_inscritos()

    def vagas_disponiveis(self, turma_id: int) -> int:
        turma = self._repo.obter_por_id(turma_id)
        if turma is None:
            raise ValueError("Turma não encontrada.")
        ocupadas = self._repo.contar_matriculas_ativas(turma_id)
        return turma._maxAlunos - ocupadas

    def tem_vagas(self, turma_id: int) -> bool:
        return self.vagas_disponiveis(turma_id) > 0

    def desativar(self, turma_id: int) -> None:
        if self._repo.obter_por_id(turma_id) is None:
            raise ValueError("Turma não encontrada.")
        if self._repo.contar_matriculas_ativas(turma_id) > 0:
            raise ValueError("Não é possível desativar uma turma com matrículas ativas. "
                             "Cancele as matrículas primeiro.")
        self._repo.desativar(turma_id)
