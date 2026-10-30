from __future__ import annotations

from db.connection import get_connection
from models.professor import Professor


class ProfessorRepository:
    def inserir(self, professor: Professor) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Professor (nome, telefone, email, custo_hora, ativo) "
                "VALUES (?, ?, ?, ?, ?)",
                (professor._nome, professor._telefone, professor._email,
                 professor._custoHora, int(professor._ativo)),
            )
            professor._id = cursor.lastrowid
            return professor._id

    def adicionar_idioma(self, professor_id: int, idioma_id: int) -> None:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO ProfessorIdioma (professor_id, idioma_id) VALUES (?, ?)",
                (professor_id, idioma_id),
            )

    def obter_por_id(self, id: int) -> Professor | None:
        with get_connection() as conn:
            linha = conn.execute(
                "SELECT * FROM Professor WHERE id = ?", (id,)
            ).fetchone()
            return self._mapear(linha) if linha else None

    def listar_todos(self) -> list[Professor]:
        with get_connection() as conn:
            linhas = conn.execute("SELECT * FROM Professor ORDER BY nome").fetchall()
            return [self._mapear(linha) for linha in linhas]

    def listar_idiomas(self, professor_id: int) -> list[int]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT idioma_id FROM ProfessorIdioma WHERE professor_id = ?",
                (professor_id,),
            ).fetchall()
            return [linha["idioma_id"] for linha in linhas]

    def desativar(self, professor_id: int) -> None:
        with get_connection() as conn:
            conn.execute(
                "UPDATE Professor SET ativo = 0 WHERE id = ?", (professor_id,)
            )

    def _mapear(self, linha) -> Professor:
        return Professor(
            id=linha["id"],
            nome=linha["nome"],
            telefone=linha["telefone"],
            email=linha["email"],
            custoHora=float(linha["custo_hora"]) if linha["custo_hora"] is not None else 0.0,
            ativo=bool(linha["ativo"]),
        )
