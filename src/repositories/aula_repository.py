from __future__ import annotations

from datetime import date

from models.aula import Aula
from db.connection import get_connection
from models.presenca import Presenca


class AulaRepository:
    def inserir(self, aula: Aula) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Aula (turma_id, professor_id, data, sumario) "
                "VALUES (?, ?, ?, ?)",
                (aula._turma._id if aula._turma else None,
                 aula._professor._id if aula._professor else None,
                 aula._data.isoformat() if aula._data else None, aula._sumario),
            )
            aula._id = cursor.lastrowid
            return aula._id

    def obter_por_id(self, id: int) -> Aula | None:
        with get_connection() as conn:
            linha = conn.execute("SELECT * FROM Aula WHERE id = ?", (id,)).fetchone()
            return self._mapear(linha) if linha else None

    def listar_por_turma(self, turma_id: int) -> list[Aula]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT * FROM Aula WHERE turma_id = ? ORDER BY data", (turma_id,)
            ).fetchall()
            return [self._mapear(linha) for linha in linhas]

    def inserir_presencas(self, aula_id: int, presencas: list[Presenca]) -> None:
        with get_connection() as conn:
            for presenca in presencas:
                conn.execute(
                    "INSERT INTO Presenca (aula_id, matricula_id, estado) "
                    "VALUES (?, ?, ?)",
                    (aula_id,
                     presenca._matricula._id if presenca._matricula else None,
                     presenca._estado),
                )

    def listar_presencas_por_aula(self, aula_id: int) -> list[Presenca]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT * FROM Presenca WHERE aula_id = ?", (aula_id,)
            ).fetchall()
            return [Presenca(id=linha["id"], estado=linha["estado"]) for linha in linhas]

    def listar_presencas_por_matricula(self, matricula_id: int) -> list[Presenca]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT * FROM Presenca WHERE matricula_id = ?", (matricula_id,)
            ).fetchall()
            return [Presenca(id=linha["id"], estado=linha["estado"]) for linha in linhas]

    def _mapear(self, linha) -> Aula:
        return Aula(
            id=linha["id"],
            data=date.fromisoformat(linha["data"]) if linha["data"] else None,
            sumario=linha["sumario"],
        )
