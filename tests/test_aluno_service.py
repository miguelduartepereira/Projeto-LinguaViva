import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from models.aluno import Aluno
from services.aluno_service import AlunoService


class TestAlunoService(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_matriculas = MagicMock()
        self.svc = AlunoService(self.mock_repo, self.mock_matriculas)
        self.nasc_adulto = date(date.today().year - 20, 6, 15)
        self.nasc_menor = date(date.today().year - 15, 6, 15)

    def _adulto(self, nome="Ana Costa", nif="123456789", email="ana@lv.pt"):
        return Aluno(0, nome, nif, self.nasc_adulto, "911222333", email)

    def _menor_valido(self):
        aluno = Aluno(0, "Jovem Silva", "222333444", self.nasc_menor,
                      email="jovem@lv.pt", consentimentoRGPD=True)
        aluno._id_encarregado = object()
        return aluno

    def test_nome_vazio_levanta_erro(self):
        aluno = self._adulto(nome="")
        with self.assertRaises(ValueError):
            self.svc.registar(aluno)
        self.mock_repo.inserir.assert_not_called()

    def test_nome_so_espacos_levanta_erro(self):
        aluno = self._adulto(nome="   ")
        with self.assertRaises(ValueError):
            self.svc.registar(aluno)
        self.mock_repo.inserir.assert_not_called()

    def test_data_nascimento_obrigatoria(self):
        aluno = Aluno(0, "Ana", "123456789", None, email="ana@lv.pt")
        with self.assertRaises(ValueError):
            self.svc.registar(aluno)
        self.mock_repo.inserir.assert_not_called()

    def test_email_invalido_levanta_erro(self):
        aluno = self._adulto(email="invalido")
        with self.assertRaises(ValueError):
            self.svc.registar(aluno)
        self.mock_repo.inserir.assert_not_called()

    # 3 · subTest — vários casos inválidos num único teste
    def test_nifs_invalidos_varios_casos(self):
        """subTest continua a testar os restantes casos mesmo que um falhe."""
        nifs_invalidos = [
            ("", "vazio"),
            ("12345", "poucos dígitos"),
            ("12345678", "8 dígitos"),
            ("1234567890", "10 dígitos"),
            ("12345678A", "com letra"),
        ]
        for nif, descricao in nifs_invalidos:
            with self.subTest(caso=descricao, nif=nif):
                with self.assertRaises(ValueError):
                    self.svc.registar(self._adulto(nif=nif))

    def test_emails_invalidos_varios_casos(self):
        emails_invalidos = [
            ("semArroba", "sem @"),
            ("ana@lv", "domínio sem ponto"),
            ("ana@", "sem domínio"),
        ]
        for email, descricao in emails_invalidos:
            with self.subTest(caso=descricao, email=email):
                with self.assertRaises(ValueError):
                    self.svc.registar(self._adulto(email=email))

    def test_menor_sem_encarregado_levanta_erro(self):
        aluno = Aluno(0, "Jovem", "222333444", self.nasc_menor,
                      email="j@lv.pt", consentimentoRGPD=True)
        with self.assertRaises(ValueError):
            self.svc.registar(aluno)
        self.mock_repo.inserir.assert_not_called()

    def test_menor_sem_consentimento_levanta_erro(self):
        aluno = Aluno(0, "Jovem", "222333444", self.nasc_menor, email="j@lv.pt")
        aluno._id_encarregado = object()
        with self.assertRaises(ValueError):
            self.svc.registar(aluno)
        self.mock_repo.inserir.assert_not_called()

    def test_menor_valido_e_aceite(self):
        self.svc.registar(self._menor_valido())
        self.mock_repo.inserir.assert_called_once()

    def test_adulto_nao_precisa_de_rgpd(self):
        """Maior de idade sem encarregado nem consentimento deve ser aceite."""
        self.svc.registar(self._adulto())
        self.mock_repo.inserir.assert_called_once()

    # 5 · Caminho feliz — call_args para inspecionar o objeto
    def test_registar_chama_repo_uma_vez(self):
        self.svc.registar(self._adulto())
        self.mock_repo.inserir.assert_called_once()

    def test_registar_passa_aluno_correto_ao_repo(self):
        self.svc.registar(self._adulto("Ana Costa", "123456789", "ana@lv.pt"))
        aluno = self.mock_repo.inserir.call_args[0][0]
        self.assertEqual(aluno._nome, "Ana Costa")
        self.assertEqual(aluno._nif, "123456789")
        self.assertEqual(aluno._email, "ana@lv.pt")

    def test_registar_devolve_id_do_repo(self):
        """return_value simula o id gerado pela base de dados."""
        self.mock_repo.inserir.return_value = 99
        resultado = self.svc.registar(self._adulto())
        self.assertEqual(resultado, 99)

    # 6 · Pesquisa / listagem — assert_called_once_with + return_value
    def test_pesquisar_chama_repo_com_termo(self):
        self.svc.pesquisar("Ana")
        self.mock_repo.pesquisar.assert_called_once_with("Ana")

    def test_pesquisar_faz_strip_do_termo(self):
        self.svc.pesquisar("   Ana   ")
        self.mock_repo.pesquisar.assert_called_once_with("Ana")

    def test_pesquisar_sem_termo_lista_todos(self):
        """Termo vazio deve devolver todos os alunos, sem chamar pesquisar."""
        self.svc.pesquisar("")
        self.mock_repo.listar_todos.assert_called_once()
        self.mock_repo.pesquisar.assert_not_called()

    def test_pesquisar_devolve_lista_do_repo(self):
        turma = [self._adulto("Ana"), self._adulto("Bruno")]
        self.mock_repo.pesquisar.return_value = turma
        resultado = self.svc.pesquisar("a")
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[1]._nome, "Bruno")

    def test_listar_devolve_lista_do_repo(self):
        self.mock_repo.listar_todos.return_value = [self._adulto()]
        resultado = self.svc.listar()
        self.assertEqual(len(resultado), 1)
        self.mock_repo.listar_todos.assert_called_once()

    def test_obter_inexistente_devolve_none(self):
        self.mock_repo.obter_por_id.return_value = None
        self.assertIsNone(self.svc.obter(123))
        self.mock_repo.obter_por_id.assert_called_once_with(123)

    # 7 · Histórico (RF11) — orquestração de dois repositórios
    def test_obter_historico_chama_repo_matriculas(self):
        self.svc.obter_historico(5)
        self.mock_matriculas.listar_por_aluno.assert_called_once_with(5)

    def test_obter_historico_aluno_inexistente_levanta_erro(self):
        self.mock_repo.obter_por_id.return_value = None
        with self.assertRaises(ValueError):
            self.svc.obter_historico(999)
        self.mock_matriculas.listar_por_aluno.assert_not_called()

    def test_obter_historico_devolve_lista_do_repo(self):
        self.mock_matriculas.listar_por_aluno.return_value = [MagicMock(), MagicMock()]
        resultado = self.svc.obter_historico(5)
        self.assertEqual(len(resultado), 2)

    def test_erro_db_propaga_excecao(self):
        """Se o repositório falhar, o serviço não deve engolir o erro."""
        self.mock_repo.inserir.side_effect = RuntimeError("Ligação à BD perdida")
        with self.assertRaises(RuntimeError):
            self.svc.registar(self._adulto())

    def test_registar_dois_alunos_em_sequencia(self):
        self.mock_repo.inserir.side_effect = [10, 20]
        r1 = self.svc.registar(self._adulto("Ana", "123456789"))
        r2 = self.svc.registar(self._adulto("Bruno", "987654321"))
        self.assertEqual(r1, 10)
        self.assertEqual(r2, 20)
        self.assertEqual(self.mock_repo.inserir.call_count, 2)


if __name__ == "__main__":
    unittest.main()
