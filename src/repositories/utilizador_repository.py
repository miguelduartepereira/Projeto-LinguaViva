from __future__ import annotations

from db.connection import get_connection
from models.utilizador import Utilizador


class UtilizadorRepository:
    def inserir(self, utilizador: Utilizador) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Utilizador (username, password_hash, perfil, "
                "professor_id, ativo) VALUES (?, ?, ?, ?, ?)",
                (utilizador._username, utilizador._passwordHash, utilizador._perfil,
                 utilizador._professor._id if utilizador._professor else None,
                 int(utilizador._ativo)),
            )
            utilizador._id = cursor.lastrowid
            return utilizador._id

    def obter_por_username(self, username: str) -> Utilizador | None:
        with get_connection() as conn:
            linha = conn.execute(
                "SELECT * FROM Utilizador WHERE username = ?", (username,)
            ).fetchone()
            return self._mapear(linha) if linha else None

    def _mapear(self, linha) -> Utilizador:
        return Utilizador(
            id=linha["id"],
            username=linha["username"],
            passwordHash=linha["password_hash"],
            perfil=linha["perfil"],
            ativo=bool(linha["ativo"]),
        )
