from __future__ import annotations

from models.professor import Professor
from repositories.professor_repository import ProfessorRepository
from repositories.turma_repository import TurmaRepository


class ProfessorService:
    def __init__(self):
        self._repo = ProfessorRepository()
        self._turmas = TurmaRepository()

    def registar(self, professor: Professor, idiomas: list[int] | None = None) -> int:
        if not professor._nome or not professor._nome.strip():
            raise ValueError("O nome do professor é obrigatório.")
        if professor._custoHora < 0:
            raise ValueError("O custo por hora não pode ser negativo.")
        professor_id = self._repo.inserir(professor)
        for idioma_id in (idiomas or []):
            self._repo.adicionar_idioma(professor_id, idioma_id)
        return professor_id

    def associar_idioma(self, professor_id: int, idioma_id: int) -> None:
        if self._repo.obter_por_id(professor_id) is None:
            raise ValueError("Professor não encontrado.")
        self._repo.adicionar_idioma(professor_id, idioma_id)

    def desativar(self, professor_id: int) -> None:
        if self._repo.obter_por_id(professor_id) is None:
            raise ValueError("Professor não encontrado.")
        turmas = self._turmas.listar_por_professor(professor_id)
        if any(turma._ativa for turma in turmas):
            raise ValueError("Não é possível desativar um professor com turmas ativas.")
        self._repo.desativar(professor_id)

    def obter(self, professor_id: int) -> Professor | None:
        return self._repo.obter_por_id(professor_id)

    def listar(self) -> list[Professor]:
        return self._repo.listar_todos()

    def listar_idiomas(self, professor_id: int) -> list[int]:
        return self._repo.listar_idiomas(professor_id)
