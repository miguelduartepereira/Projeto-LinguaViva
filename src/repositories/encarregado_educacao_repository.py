from __future__ import annotations

from db.connection import get_connection
from models.encarregado_educacao import EncarregadoEducacao


class EncarregadoEducacaoRepository:
    def inserir(self, encarregado: EncarregadoEducacao) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO EncarregadoEducacao (nome, nif, telefone, email, parentesco) "
                "VALUES (?, ?, ?, ?, ?)",
                (encarregado._nome, encarregado._nif, encarregado._telefone,
                 encarregado._email, encarregado._parentesco),
            )
            encarregado._id = cursor.lastrowid
            return encarregado._id

    def obter_por_id(self, id: int) -> EncarregadoEducacao | None:
        with get_connection() as conn:
            linha = conn.execute(
                "SELECT * FROM EncarregadoEducacao WHERE id = ?", (id,)
            ).fetchone()
            if not linha:
                return None
            return EncarregadoEducacao(
                id=linha["id"],
                nome=linha["nome"],
                nif=linha["nif"],
                telefone=linha["telefone"],
                email=linha["email"],
                parentesco=linha["parentesco"],
            )
