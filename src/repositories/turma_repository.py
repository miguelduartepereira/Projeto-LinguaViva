from __future__ import annotations

from db.connection import get_connection
from models.turma import Turma


class TurmaRepository:
    def inserir(self, turma: Turma) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Turma (idioma_id, nivel_id, professor_id, horario, sala, "
                "max_alunos, semestre, ano, ativa) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (turma._idioma._id if turma._idioma else None,
                 turma._nivel._id if turma._nivel else None,
                 turma._professor._id if turma._professor else None,
                 turma._horario, turma._sala, turma._maxAlunos,
                 turma._semestre, turma._ano, int(turma._ativa)),
            )
            turma._id = cursor.lastrowid
            return turma._id

    def obter_por_id(self, id: int) -> Turma | None:
        with get_connection() as conn:
            linha = conn.execute("SELECT * FROM Turma WHERE id = ?", (id,)).fetchone()
            return self._mapear(linha) if linha else None

    def listar_todas(self) -> list[Turma]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT * FROM Turma ORDER BY ano, semestre"
            ).fetchall()
            return [self._mapear(linha) for linha in linhas]

    def listar_com_inscritos(self) -> list[dict]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT t.id, t.horario, t.sala, t.max_alunos, "
                "COUNT(CASE WHEN m.estado = 'ativa' THEN 1 END) AS inscritos "
                "FROM Turma t LEFT JOIN Matricula m ON m.turma_id = t.id "
                "GROUP BY t.id, t.horario, t.sala, t.max_alunos ORDER BY t.id"
            ).fetchall()
            return [
                {"id": linha["id"], "horario": linha["horario"], "sala": linha["sala"],
                 "max_alunos": linha["max_alunos"], "inscritos": linha["inscritos"]}
                for linha in linhas
            ]

    def _mapear(self, linha) -> Turma:
        return Turma(
            id=linha["id"],
            horario=linha["horario"],
            sala=linha["sala"],
            maxAlunos=linha["max_alunos"],
            semestre=linha["semestre"],
            ano=linha["ano"],
            ativa=bool(linha["ativa"]),
        )
