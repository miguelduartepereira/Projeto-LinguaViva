# tests/test_auth_service.py — testes do Lab 1 (bcrypt) e Lab 2 (JWT)
import os
import sys
import unittest
from unittest.mock import MagicMock

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "src"))

import jwt
from models.utilizador import Utilizador
from services.auth_service import AuthService, SECRET_KEY


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.repo.obter_por_username.return_value = None
        self.auth = AuthService(self.repo)

    def registar_e_obter(self, senha="Segura#2026", perfil="Secretaria"):
        self.auth.registar("ana", senha, perfil)
        guardado = self.repo.inserir.call_args[0][0]   # o Utilizador enviado ao repositório
        self.repo.obter_por_username.return_value = guardado
        return guardado

    # ----- Lab 1: bcrypt
    def test_password_guardada_com_bcrypt(self):
        u = self.registar_e_obter()
        self.assertTrue(u._passwordHash.startswith("$2b$12$"))
        self.assertNotIn("Segura#2026", u._passwordHash)

    def test_mesma_password_da_hashes_diferentes(self):
        self.auth.registar("a", "Segura#2026", "Secretaria")
        self.auth.registar("b", "Segura#2026", "Secretaria")
        h1 = self.repo.inserir.call_args_list[0][0][0]._passwordHash
        h2 = self.repo.inserir.call_args_list[1][0][0]._passwordHash
        self.assertNotEqual(h1, h2)   # salt diferente

    def test_login_correto(self):
        self.registar_e_obter()
        u = self.auth.autenticar("ana", "Segura#2026")
        self.assertEqual(u._perfil, "Secretaria")

    def test_password_errada(self):
        self.registar_e_obter()
        with self.assertRaises(ValueError):
            self.auth.autenticar("ana", "errada123")

    def test_utilizador_inexistente_mesma_mensagem(self):
        with self.assertRaises(ValueError) as erro:
            self.auth.autenticar("ninguem", "qualquer123")
        self.assertEqual(str(erro.exception), "Credenciais inválidas.")

    def test_conta_desativada(self):
        u = self.registar_e_obter()
        u._ativo = False
        with self.assertRaises(ValueError):
            self.auth.autenticar("ana", "Segura#2026")

    def test_password_curta_e_perfil_invalido(self):
        with self.assertRaises(ValueError):
            self.auth.registar("ana", "123", "Secretaria")
        with self.assertRaises(ValueError):
            self.auth.registar("ana", "Segura#2026", "Admin")

    def test_utilizador_repetido(self):
        self.repo.obter_por_username.return_value = Utilizador(1, "ana", "x", "Secretaria")
        with self.assertRaises(ValueError):
            self.auth.registar("ana", "Segura#2026", "Secretaria")

    # ----- Lab 2: JWT
    def test_token_tem_perfil_e_expira(self):
        u = self.registar_e_obter(perfil="Direcao")
        dados = self.auth.validar_token(self.auth.criar_token(u))
        self.assertEqual(dados["sub"], "ana")
        self.assertEqual(dados["perfil"], "direcao")
        self.assertEqual(dados["exp"] - dados["iat"], 8 * 3600)

    def test_token_alterado_e_rejeitado(self):
        u = self.registar_e_obter()
        token = self.auth.criar_token(u)
        falso = jwt.encode({"sub": "ana", "perfil": "direcao", "iss": "linguaviva"},
                           "outra-chave-qualquer-com-32-caracteres", algorithm="HS256")
        with self.assertRaises(PermissionError):
            self.auth.validar_token(falso)
        with self.assertRaises(PermissionError):
            self.auth.validar_token(token[:-3] + "abc")

    def test_validar_token_sem_criar_objeto(self):
        # o rbac.py chama AuthService.validar_token(token) diretamente na classe
        u = self.registar_e_obter(perfil="Professor")
        dados = AuthService.validar_token(self.auth.criar_token(u))
        self.assertEqual(dados["perfil"], "professor")

    def test_token_expirado(self):
        expirado = jwt.encode({"sub": "ana", "perfil": "secretaria", "iss": "linguaviva", "exp": 1},
                              SECRET_KEY, algorithm="HS256")
        with self.assertRaises(PermissionError):
            self.auth.validar_token(expirado)


if __name__ == "__main__":
    unittest.main()
