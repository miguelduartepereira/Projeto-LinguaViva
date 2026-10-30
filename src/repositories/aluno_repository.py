from __future__ import annotations

from datetime import date

from models.aluno import Aluno
from db.connection import get_connection

class AlunoRepository:
    def inserir(self, aluno: Aluno) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO Aluno (nome, nif, data_nasc, telefone, email, morada, "
                "enc_educacao_id, consentimento_rgpd, ativo) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (aluno._nome, aluno._nif,
                 aluno._dataNasc.isoformat() if aluno._dataNasc else None,
                 aluno._telefone, aluno._email, aluno._morada,
                 aluno._id_encarregado._id if aluno._id_encarregado else None,
                 int(aluno._consentimentoRGPD), int(aluno._ativo)),
            )
            aluno._id = cursor.lastrowid
            return aluno._id

    def arquivar(self, aluno_id: int) -> None:
        with get_connection() as conn:
            conn.execute("UPDATE Aluno SET ativo = 0 WHERE id = ?", (aluno_id,))

    def obter_por_id(self, id: int) -> Aluno | None:
        with get_connection() as conn:
            linha = conn.execute("SELECT * FROM Aluno WHERE id = ?", (id,)).fetchone()
            return self._mapear(linha) if linha else None

    def pesquisar(self, termo: str) -> list[Aluno]:
        with get_connection() as conn:
            linhas = conn.execute(
                "SELECT * FROM Aluno WHERE nome LIKE ? OR nif = ? ORDER BY nome",
                (f"%{termo}%", termo),
            ).fetchall()
            return [self._mapear(linha) for linha in linhas]

    def listar_todos(self) -> list[Aluno]:
        with get_connection() as conn:
            linhas = conn.execute("SELECT * FROM Aluno ORDER BY nome").fetchall()
            return [self._mapear(linha) for linha in linhas]

    def _mapear(self, linha) -> Aluno:
        return Aluno(
            id=linha["id"],
            nome=linha["nome"],
            nif=linha["nif"],
            dataNasc=date.fromisoformat(linha["data_nasc"]) if linha["data_nasc"] else None,
            telefone=linha["telefone"],
            email=linha["email"],
            morada=linha["morada"],
            consentimentoRGPD=bool(linha["consentimento_rgpd"]),
            ativo=bool(linha["ativo"]),
        )
