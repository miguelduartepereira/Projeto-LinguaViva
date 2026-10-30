from __future__ import annotations

class Utilizador:
    def __init__(self, id: int, username: str, passwordHash: str,
                 perfil: str, ativo: bool = True):
        self._id = id
        self._username = username
        self._passwordHash = passwordHash
        self._perfil = perfil
        self._ativo = ativo
        self._professor: Professor | None = None


    def temPermissao(self, acao: str) -> bool:
        permissoes = {
            "Secretaria": {"registarAluno", "registarProfessor", "criarTurma",
                           "matricularAluno", "cancelarMatricula", "pesquisarAluno",
                           "listarTurmas", "emitirCertificado", "exportarPauta"},
            "Professor": {"registarAula", "registarPresencas", "registarAvaliacao"},
            "Direcao": {"consultarRelatorioAssiduidade", "consultarRelatorioAprovados"},
        }
        return acao in permissoes.get(self._perfil, set())
