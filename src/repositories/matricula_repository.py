from __future__ import annotations

from datetime import date

from models.avaliacao import Avaliacao
from models.certificado import Certificado
from db.connection import get_connection
from models.matricula import Matricula


class MatriculaRepository:
    def inserir(self, matricula: Matricula) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Matricula (aluno_id, turma_id, data_matricula, "
                "valor_propina, estado, nota_final) VALUES (?, ?, ?, ?, ?, ?)",
                (matricula._aluno._id if matricula._aluno else None,
                 matricula._turma._id if matricula._turma else None,
                 matricula._dataMatricula.isoformat() if matricula._dataMatricula else None,
                 matricula._valorPropina, matricula._estado, matricula._notaFinal),
            )
            matricula._id = cursor.lastrowid
            return matricula._id

    def cancelar(self, matricula_id: int) -> None:
        with get_connection() as conn:
            conn.execute(
                "UPDATE Matricula SET estado = 'cancelada' WHERE id = ?",
                (matricula_id,),
            )

    def atualizar_nota_final(self, matricula_id: int, nota_final: float) -> None:
        with get_connection() as conn:
            conn.execute(
                "UPDATE Matricula SET nota_final = ?, estado = 'concluida' WHERE id = ?",
                (nota_final, matricula_id),
            )

    def obter_por_id(self, id: int) -> Matricula | None:
        with get_connection() as conn:
            linha = conn.execute(
                "SELECT * FROM Matricula WHERE id = ?", (id,)
            ).fetchone()
            return self._mapear(linha) if linha else None

    def listar_por_turma(self, turma_id: int) -> list[Matricula]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT * FROM Matricula WHERE turma_id = ? ORDER BY id", (turma_id,)
            ).fetchall()
            return [self._mapear(linha) for linha in linhas]

    def listar_por_aluno(self, aluno_id: int) -> list[Matricula]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT * FROM Matricula WHERE aluno_id = ? ORDER BY id", (aluno_id,)
            ).fetchall()
            return [self._mapear(linha) for linha in linhas]

    def inserir_avaliacao(self, matricula_id: int, avaliacao: Avaliacao) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Avaliacao (matricula_id, tipo, nota, data) "
                "VALUES (?, ?, ?, ?)",
                (matricula_id, avaliacao._tipo, avaliacao._nota,
                 avaliacao._data.isoformat() if avaliacao._data else None),
            )
            avaliacao._id = cursor.lastrowid
            return avaliacao._id

    def listar_avaliacoes(self, matricula_id: int) -> list[Avaliacao]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT * FROM Avaliacao WHERE matricula_id = ?", (matricula_id,)
            ).fetchall()
            return [
                Avaliacao(
                    id=linha["id"],
                    tipo=linha["tipo"],
                    nota=float(linha["nota"]),
                    data=date.fromisoformat(linha["data"]) if linha["data"] else None,
                )
                for linha in linhas
            ]

    def inserir_certificado(self, matricula_id: int, certificado: Certificado) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Certificado (matricula_id, numero_certificado, "
                "data_emissao, ficheiro_pdf) VALUES (?, ?, ?, ?)",
                (matricula_id, certificado._numero,
                 certificado._dataEmissao.isoformat() if certificado._dataEmissao else None,
                 certificado._ficheiroPdf),
            )
            certificado._id = cursor.lastrowid
            return certificado._id

    def obter_certificado(self, matricula_id: int) -> Certificado | None:
        with get_connection() as conn:
            linha = conn.execute(
                "SELECT * FROM Certificado WHERE matricula_id = ?", (matricula_id,)
            ).fetchone()
            if not linha:
                return None
            return Certificado(
                id=linha["id"],
                numero=linha["numero_certificado"],
                dataEmissao=date.fromisoformat(linha["data_emissao"]) if linha["data_emissao"] else None,
                ficheiroPdf=linha["ficheiro_pdf"],
            )

    def _mapear(self, linha) -> Matricula:
        return Matricula(
            id=linha["id"],
            dataMatricula=date.fromisoformat(linha["data_matricula"]) if linha["data_matricula"] else None,
            valorPropina=float(linha["valor_propina"]) if linha["valor_propina"] is not None else 0.0,
            estado=linha["estado"],
            notaFinal=float(linha["nota_final"]) if linha["nota_final"] is not None else None,
        )
