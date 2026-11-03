from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from db.connection import inicializar_bd
from models.aluno import Aluno
from models.aula import Aula
from models.avaliacao import Avaliacao
from models.encarregado_educacao import EncarregadoEducacao
from models.idioma import Idioma
from models.matricula import Matricula
from models.nivel import Nivel
from models.presenca import Presenca
from models.professor import Professor
from models.turma import Turma
from repositories.aula_repository import AulaRepository
from repositories.encarregado_educacao_repository import EncarregadoEducacaoRepository
from repositories.matricula_repository import MatriculaRepository
from services.aluno_service import AlunoService
from services.aula_service import AulaService
from services.idioma_service import IdiomaService
from services.matricula_service import MatriculaService
from services.nivel_service import NivelService
from services.professor_service import ProfessorService
from services.turma_service import TurmaService

idioma_service = IdiomaService()
nivel_service = NivelService()
professor_service = ProfessorService()
turma_service = TurmaService()
aluno_service = AlunoService()
matricula_service = MatriculaService()
aula_service = AulaService()
encarregado_repo = EncarregadoEducacaoRepository()
matricula_repo = MatriculaRepository()
aula_repo = AulaRepository()


def ler(texto: str) -> str:
    return input(texto).strip()


def ler_int(texto: str):
    valor = input(texto).strip()
    return int(valor) if valor.lstrip("-").isdigit() else None


def ler_float(texto: str):
    valor = input(texto).strip().replace(",", ".")
    try:
        return float(valor)
    except ValueError:
        return None


def ler_data(texto: str):
    valor = input(texto).strip()
    try:
        return date.fromisoformat(valor)
    except ValueError:
        return None


def pausa() -> None:
    input("\n(Enter para continuar) ")


def e_menor(data_nasc: date) -> bool:
    hoje = date.today()
    idade = hoje.year - data_nasc.year - (
        (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day)
    )
    return idade < 18


def escolher(itens, rotulo, titulo):
    if not itens:
        print(f"Nao ha {titulo.lower()} disponiveis.")
        return None
    print(f"\n{titulo}:")
    for item in itens:
        print(f"  {item._id}. {rotulo(item)}")
    escolha = ler_int("Id (0 cancela): ")
    if not escolha:
        return None
    for item in itens:
        if item._id == escolha:
            return item
    print("Id invalido.")
    return None


def rotulo_turma(turma) -> str:
    idioma = turma._idioma._codigo if turma._idioma else "?"
    nivel = turma._nivel._codigo if turma._nivel else "?"
    estado = "ativa" if turma._ativa else "inativa"
    return f"{idioma} {nivel} | {turma._horario} | sala {turma._sala} | {estado}"


def loop_menu(titulo, opcoes, pausar=True):
    while True:
        print(f"\n==== {titulo} ====")
        for chave, (rotulo, _) in opcoes.items():
            print(f"  {chave}. {rotulo}")
        print("  0. Sair/Voltar")
        escolha = ler("Opcao: ")
        if escolha == "0":
            return
        accao = opcoes.get(escolha)
        if accao is None:
            print("Opcao invalida.")
            continue
        try:
            accao[1]()
        except ValueError as erro:
            print(f"Erro: {erro}")
        except Exception as erro:
            print(f"Erro inesperado: {erro}")
        if pausar:
            pausa()


def registar_idioma():
    nome = ler("Nome do idioma: ")
    codigo = ler("Codigo (EN/FR/...): ")
    novo_id = idioma_service.registar(Idioma(0, nome, codigo))
    print(f"OK Idioma registado com id {novo_id}.")


def registar_nivel():
    codigo = ler("Codigo (A1-C2): ")
    descricao = ler("Descricao: ")
    oral = ler_float("Ponderacao oral (ex: 0.3): ")
    escrito = ler_float("Ponderacao escrito: ")
    projeto = ler_float("Ponderacao projeto: ")
    if None in (oral, escrito, projeto):
        print("Ponderacoes invalidas.")
        return
    novo_id = nivel_service.registar(Nivel(0, codigo, descricao, oral, escrito, projeto))
    print(f"OK Nivel registado com id {novo_id}.")


def registar_professor():
    nome = ler("Nome: ")
    telefone = ler("Telefone: ")
    email = ler("Email: ")
    custo = ler_float("Custo por hora: ")
    if custo is None:
        print("Custo invalido.")
        return
    idiomas = idioma_service.listar()
    ids = []
    if idiomas:
        print("Idiomas que leciona:")
        for idioma in idiomas:
            print(f"  {idioma._id}. {idioma._nome} ({idioma._codigo})")
        escolha = ler("Ids separados por virgula (Enter p/ nenhum): ")
        ids = [int(x) for x in escolha.replace(" ", "").split(",") if x.isdigit()]
    novo_id = professor_service.registar(Professor(0, nome, telefone, email, custo, True), idiomas=ids)
    print(f"OK Professor registado com id {novo_id}.")


def registar_aluno():
    nome = ler("Nome: ")
    nif = ler("NIF (9 digitos): ")
    data_nasc = ler_data("Data de nascimento (AAAA-MM-DD): ")
    if data_nasc is None:
        print("Data invalida.")
        return
    telefone = ler("Telefone: ")
    email = ler("Email: ")
    morada = ler("Morada: ")
    aluno = Aluno(0, nome, nif, data_nasc, telefone, email, morada)
    if e_menor(data_nasc):
        print("Aluno menor de idade - dados do encarregado (RGPD):")
        enc_nome = ler("  Nome do encarregado: ")
        enc_nif = ler("  NIF: ")
        enc_telefone = ler("  Telefone: ")
        enc_email = ler("  Email: ")
        enc_parentesco = ler("  Parentesco: ")
        consentimento = ler("  Consentimento RGPD? (s/n): ").lower() == "s"
        encarregado = EncarregadoEducacao(0, enc_nome, enc_nif, enc_telefone, enc_email, enc_parentesco)
        encarregado_repo.inserir(encarregado)
        aluno._id_encarregado = encarregado
        aluno._consentimentoRGPD = consentimento
    novo_id = aluno_service.registar(aluno)
    print(f"OK Aluno registado com id {novo_id}.")


def criar_turma():
    idioma = escolher(idioma_service.listar(), lambda i: f"{i._nome} ({i._codigo})", "Idioma")
    if not idioma:
        return
    nivel = escolher(nivel_service.listar(), lambda n: f"{n._codigo} - {n._descricao}", "Nivel")
    if not nivel:
        return
    professor = escolher(professor_service.listar(), lambda p: p._nome, "Professor")
    if not professor:
        return
    horario = ler("Horario (ex: Seg 18h): ")
    sala = ler("Sala: ")
    maximo = ler_int("Numero maximo de alunos (6-12): ")
    semestre = ler_int("Semestre (1 ou 2): ")
    ano = ler_int("Ano: ")
    if None in (maximo, semestre, ano):
        print("Valores invalidos.")
        return
    turma = Turma(0, horario, sala, maximo, semestre, ano, True)
    turma._idioma, turma._nivel, turma._professor = idioma, nivel, professor
    novo_id = turma_service.criar(turma)
    print(f"OK Turma criada com id {novo_id}.")


def matricular_aluno():
    aluno = escolher(aluno_service.listar(), lambda a: f"{a._nome} (NIF {a._nif})", "Aluno")
    if not aluno:
        return
    turma = escolher(turma_service.listar(), rotulo_turma, "Turma")
    if not turma:
        return
    propina = ler_float("Valor da propina: ")
    matricula = Matricula(0, date.today(), propina or 0.0)
    matricula._aluno, matricula._turma = aluno, turma
    novo_id = matricula_service.matricular(matricula)
    print(f"OK Matricula criada com id {novo_id}.")


def pesquisar_aluno():
    termo = ler("Nome ou NIF: ")
    resultados = aluno_service.pesquisar(termo)
    if not resultados:
        print("Sem resultados.")
        return
    for aluno in resultados:
        estado = "ativo" if aluno._ativo else "arquivado"
        print(f"  [{aluno._id}] {aluno._nome} | NIF {aluno._nif} | {aluno._email} | {estado}")


def listar_turmas():
    linhas = turma_service.listar_com_inscritos()
    if not linhas:
        print("Sem turmas.")
        return
    for turma in linhas:
        print(f"  [{turma['id']}] {turma['horario']} | sala {turma['sala']} | "
              f"{turma['inscritos']}/{turma['max_alunos']} inscritos")


def fechar_nota_final():
    turma = escolher(turma_service.listar(), rotulo_turma, "Turma")
    if not turma:
        return
    matriculas = matricula_repo.listar_por_turma(turma._id)
    matricula = escolher(matriculas, lambda m: f"matricula {m._id} | estado {m._estado}", "Matricula")
    if not matricula:
        return
    matricula._turma = turma
    nota = matricula_service.calcular_nota_final(matricula)
    print(f"OK Nota final = {nota}")


def emitir_certificado():
    turma = escolher(turma_service.listar(), rotulo_turma, "Turma")
    if not turma:
        return
    matriculas = matricula_repo.listar_por_turma(turma._id)
    matricula = escolher(
        matriculas,
        lambda m: f"matricula {m._id} | estado {m._estado} | nota {m._notaFinal}",
        "Matricula",
    )
    if not matricula:
        return
    matricula._turma = turma
    certificado = matricula_service.emitir_certificado(matricula)
    print(f"OK Certificado emitido: {certificado._numero} ({certificado._ficheiroPdf})")


def registar_aula():
    turma = escolher(turma_service.listar(), rotulo_turma, "Turma")
    if not turma:
        return
    data_aula = ler_data("Data (AAAA-MM-DD): ")
    if data_aula is None:
        print("Data invalida.")
        return
    sumario = ler("Sumario: ")
    professor = turma._professor
    if ler("Houve substituicao de professor? (s/n): ").lower() == "s":
        substituto = escolher(professor_service.listar(), lambda p: p._nome, "Professor substituto")
        professor = substituto or turma._professor
    aula = Aula(0, data_aula, sumario)
    aula._turma, aula._professor = turma, professor
    novo_id = aula_service.registar(aula)
    print(f"OK Aula registada com id {novo_id}.")


def registar_presencas():
    turma = escolher(turma_service.listar(), rotulo_turma, "Turma")
    if not turma:
        return
    aulas = aula_repo.listar_por_turma(turma._id)
    aula = escolher(aulas, lambda a: f"aula {a._id} | {a._data} | {a._sumario}", "Aula")
    if not aula:
        return
    matriculas = [m for m in matricula_repo.listar_por_turma(turma._id) if m._estado == "ativa"]
    if not matriculas:
        print("Sem matriculas ativas nesta turma.")
        return
    print("Estado: P=Presente, A=Ausente, J=Justificado")
    presencas = []
    for matricula in matriculas:
        estado = ler(f"  Matricula {matricula._id} [P/A/J]: ").upper() or "A"
        presenca = Presenca(0, estado)
        presenca._matricula = matricula
        presencas.append(presenca)
    aula_service.registar_presencas(aula._id, presencas)
    print(f"OK {len(presencas)} presencas registadas.")


def registar_avaliacao():
    turma = escolher(turma_service.listar(), rotulo_turma, "Turma")
    if not turma:
        return
    matriculas = matricula_repo.listar_por_turma(turma._id)
    matricula = escolher(matriculas, lambda m: f"matricula {m._id} | estado {m._estado}", "Matricula")
    if not matricula:
        return
    tipo = ler("Tipo (oral/escrito/projeto): ").lower()
    nota = ler_float("Nota (0-20): ")
    if nota is None:
        print("Nota invalida.")
        return
    data_av = ler_data("Data (AAAA-MM-DD): ")
    if data_av is None:
        print("Data invalida.")
        return
    matricula_service.registar_avaliacao(matricula._id, Avaliacao(0, tipo, nota, data_av))
    print("OK Avaliacao registada.")


def relatorio_assiduidade():
    turma = escolher(turma_service.listar(), rotulo_turma, "Turma")
    if not turma:
        return
    matriculas = matricula_repo.listar_por_turma(turma._id)
    if not matriculas:
        print("Turma sem matriculas.")
        return
    print(f"\nAssiduidade - turma {turma._id}:")
    for matricula in matriculas:
        taxa = matricula_service.calcular_assiduidade(matricula)
        risco = "   <-- EM RISCO" if taxa < 80 else ""
        print(f"  matricula {matricula._id}: {taxa:.1f}%{risco}")


def relatorio_aprovados():
    turma = escolher(turma_service.listar(), rotulo_turma, "Turma")
    if not turma:
        return
    matriculas = matricula_repo.listar_por_turma(turma._id)
    if not matriculas:
        print("Turma sem matriculas.")
        return
    aprovados, reprovados = [], []
    for matricula in matriculas:
        taxa = matricula_service.calcular_assiduidade(matricula)
        nota = matricula._notaFinal
        if nota is not None and taxa >= 75 and nota >= 10:
            aprovados.append(matricula._id)
        else:
            reprovados.append(matricula._id)
    print(f"\nTurma {turma._id}:")
    print(f"  Aprovados: {aprovados or '-'}")
    print(f"  Reprovados/pendentes: {reprovados or '-'}")


def consultar_educando():
    termo = ler("Nome ou NIF do educando: ")
    resultados = aluno_service.pesquisar(termo)
    if not resultados:
        print("Sem resultados.")
        return
    aluno = resultados[0] if len(resultados) == 1 else escolher(
        resultados, lambda a: f"{a._nome} (NIF {a._nif})", "Aluno"
    )
    if not aluno:
        return
    historico = aluno_service.obter_historico(aluno._id)
    print(f"\nHistorico de {aluno._nome}:")
    if not historico:
        print("  (sem matriculas)")
        return
    for matricula in historico:
        print(f"  matricula {matricula._id} | estado {matricula._estado} | "
              f"nota final {matricula._notaFinal}")


def menu_secretaria():
    loop_menu("Menu Secretaria", {
        "1": ("Registar aluno", registar_aluno),
        "2": ("Registar professor", registar_professor),
        "3": ("Registar idioma", registar_idioma),
        "4": ("Registar nivel", registar_nivel),
        "5": ("Criar turma", criar_turma),
        "6": ("Matricular aluno", matricular_aluno),
        "7": ("Pesquisar aluno", pesquisar_aluno),
        "8": ("Listar turmas", listar_turmas),
        "9": ("Fechar nota final", fechar_nota_final),
        "10": ("Emitir certificado", emitir_certificado),
    })


def menu_professor():
    loop_menu("Menu Professor", {
        "1": ("Registar aula", registar_aula),
        "2": ("Registar presencas", registar_presencas),
        "3": ("Realizar avaliacao", registar_avaliacao),
    })


def menu_direcao():
    loop_menu("Menu Direcao", {
        "1": ("Relatorio de assiduidade", relatorio_assiduidade),
        "2": ("Relatorio de aprovados", relatorio_aprovados),
        "3": ("Listar turmas", listar_turmas),
    })


def menu_encarregado():
    loop_menu("Menu Encarregado de Educacao", {
        "1": ("Consultar historico do educando", consultar_educando),
    })


def main():
    inicializar_bd()
    print("=== Sistema de Gestao LinguaViva ===")
    loop_menu("Menu Principal", {
        "1": ("Menu Secretaria", menu_secretaria),
        "2": ("Menu Professor", menu_professor),
        "3": ("Menu Direcao", menu_direcao),
        "4": ("Menu Encarregado de Educacao", menu_encarregado),
    }, pausar=False)


if __name__ == "__main__":
    main()
