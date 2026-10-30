from __future__ import annotations

from db.connection import get_connection
from models.nivel import Nivel


class NivelRepository:
    def inserir(self, nivel: Nivel) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Nivel (codigo, descricao, ponderacao_oral, "
                "ponderacao_escrito, ponderacao_projeto) VALUES (?, ?, ?, ?, ?)",
                (nivel._codigo, nivel._descricao, nivel._pondOral,
                 nivel._pondEscrito, nivel._pondProjeto),
            )
            nivel._id = cursor.lastrowid
            return nivel._id

    def obter_por_id(self, id: int) -> Nivel | None:
        with get_connection() as conn:
            linha = conn.execute("SELECT * FROM Nivel WHERE id = ?", (id,)).fetchone()
            return self._mapear(linha) if linha else None

    def obter_por_codigo(self, codigo: str) -> Nivel | None:
        with get_connection() as conn:
            linha = conn.execute(
                "SELECT * FROM Nivel WHERE codigo = ?", (codigo,)
            ).fetchone()
            return self._mapear(linha) if linha else None

    def listar_todos(self) -> list[Nivel]:
        with get_connection() as conn:
            linhas = conn.execute("SELECT * FROM Nivel ORDER BY codigo").fetchall()
            return [self._mapear(linha) for linha in linhas]

    def _mapear(self, linha) -> Nivel:
        return Nivel(
            id=linha["id"],
            codigo=linha["codigo"],
            descricao=linha["descricao"],
            pondOral=float(linha["ponderacao_oral"]),
            pondEscrito=float(linha["ponderacao_escrito"]),
            pondProjeto=float(linha["ponderacao_projeto"]),
        )
