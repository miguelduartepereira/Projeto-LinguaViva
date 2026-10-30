from __future__ import annotations

from db.connection import get_connection
from models.idioma import Idioma


class IdiomaRepository:
    def inserir(self, idioma: Idioma) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Idioma (nome, codigo) VALUES (?, ?)",
                (idioma._nome, idioma._codigo),
            )
            idioma._id = cursor.lastrowid
            return idioma._id

    def obter_por_id(self, id: int) -> Idioma | None:
        with get_connection() as conn:
            linha = conn.execute("SELECT * FROM Idioma WHERE id = ?", (id,)).fetchone()
            return self._mapear(linha) if linha else None

    def obter_por_codigo(self, codigo: str) -> Idioma | None:
        with get_connection() as conn:
            linha = conn.execute(
                "SELECT * FROM Idioma WHERE codigo = ?", (codigo,)
            ).fetchone()
            return self._mapear(linha) if linha else None

    def listar_todos(self) -> list[Idioma]:
        with get_connection() as conn:
            linhas = conn.execute("SELECT * FROM Idioma ORDER BY nome").fetchall()
            return [self._mapear(linha) for linha in linhas]

    def _mapear(self, linha) -> Idioma:
        return Idioma(id=linha["id"], nome=linha["nome"], codigo=linha["codigo"])
