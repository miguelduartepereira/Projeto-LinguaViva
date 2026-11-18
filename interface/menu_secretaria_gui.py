# Menu da Secretaria
# Rui Gonçalves - Grupo 4 LinguaViva

import sys
sys.path.append(".")      # para encontrar a pasta db
sys.path.append("src")    # para encontrar models, services e repositories

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from db.connection import inicializar_bd
from models.aluno import Aluno
from models.encarregado_educacao import EncarregadoEducacao
from models.idioma import Idioma
from models.nivel import Nivel
from models.matricula import Matricula
from repositories.encarregado_educacao_repository import EncarregadoEducacaoRepository
from services.aluno_service import AlunoService
from services.matricula_service import MatriculaService
from services.turma_service import TurmaService
from services.idioma_service import IdiomaService
from services.nivel_service import NivelService

aluno_service = AlunoService()
matricula_service = MatriculaService()
turma_service = TurmaService()
idioma_service = IdiomaService()
nivel_service = NivelService()
encarregado_repo = EncarregadoEducacaoRepository()

AVISO_RGPD = ("Este registo contém dados pessoais de um menor. "
              "Certifique-se de ter autorização do encarregado de educação.")


# ---------------- funções de apoio ----------------

def e_menor(data_nasc):
    hoje = date.today()
    idade = hoje.year - data_nasc.year
    if (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day):
        idade = idade - 1
    return idade < 18


def email_valido(email):
    if "@" not in email:
        return False
    dominio = email.split("@")[1]
    return "." in dominio


def telefone_valido(telefone):
    # 9 dígitos e começa por 9 (telemóvel) ou 2 (fixo)
    if len(telefone) != 9 or not telefone.isdigit():
        return False
    return telefone[0] == "9" or telefone[0] == "2"


def listar_encarregados():
    # o repositório não tem listar, por isso vamos buscar o id 1, 2, 3... até não haver mais
    lista = []
    i = 1
    enc = encarregado_repo.obter_por_id(i)
    while enc is not None:
        lista.append(enc)
        i = i + 1
        enc = encarregado_repo.obter_por_id(i)
    return lista


def texto_turma(turma):
    idioma = "?"
    nivel = "?"
    if turma._idioma:
        idioma = turma._idioma._nome
    if turma._nivel:
        nivel = turma._nivel._codigo
    return str(turma._id) + " - " + idioma + " " + nivel + " | " + turma._horario + " | sala " + turma._sala


def criar_lista(janela):
    # Listbox com Scrollbar
    frame = tk.Frame(janela)
    frame.pack(fill="both", expand=True, padx=5, pady=5)
    scroll = tk.Scrollbar(frame)
    scroll.pack(side="right", fill="y")
    lista = tk.Listbox(frame, width=45, height=12, yscrollcommand=scroll.set, exportselection=False)
    lista.pack(side="left", fill="both", expand=True)
    scroll.config(command=lista.yview)
    return lista


# ---------------- T2.1 Menu Secretaria ----------------

def abrir_menu_secretaria(janela):
    janela.title("LinguaViva - Secretaria")
    janela.geometry("350x350")

    frame = tk.Frame(janela, padx=20, pady=15)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Menu — Secretaria", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Button(frame, text="Gerir Alunos", width=25, command=lambda: gerir_alunos(janela)).pack(pady=4)
    tk.Button(frame, text="Gerir Matrículas", width=25, command=lambda: gerir_matriculas(janela)).pack(pady=4)
    tk.Button(frame, text="Gerir Idiomas", width=25, command=lambda: gerir_idiomas(janela)).pack(pady=4)
    tk.Button(frame, text="Gerir Níveis", width=25, command=lambda: gerir_niveis(janela)).pack(pady=4)
    tk.Button(frame, text="Voltar", width=25, command=janela.destroy).pack(pady=4)


# ---------------- T2.2 e T2.3 Gerir Alunos ----------------

def gerir_alunos(janela_pai):
    jan = tk.Toplevel(janela_pai)
    jan.title("Gerir Alunos")
    jan.geometry("960x540")

    alunos = []
    encarregados = []
    ver_dados = tk.BooleanVar(value=False)     # RGPD: começa escondido
    consentimento = tk.BooleanVar(value=False)

    # ----- formulário (lado direito)
    form = tk.LabelFrame(jan, text="Dados do aluno", padx=8, pady=8)
    form.pack(side="right", fill="y", padx=8, pady=8)

    tk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w")
    e_nome = tk.Entry(form, width=30)
    e_nome.grid(row=0, column=1, columnspan=2, sticky="w", pady=2)

    tk.Label(form, text="Apelido:").grid(row=1, column=0, sticky="w")
    e_apelido = tk.Entry(form, width=30)
    e_apelido.grid(row=1, column=1, columnspan=2, sticky="w", pady=2)

    tk.Label(form, text="NIF:").grid(row=2, column=0, sticky="w")
    e_nif = tk.Entry(form, width=30)
    e_nif.grid(row=2, column=1, columnspan=2, sticky="w", pady=2)

    tk.Label(form, text="Data nasc. (AAAA-MM-DD):").grid(row=3, column=0, sticky="w")
    e_data = tk.Entry(form, width=30, show="*")    # escondida por causa do RGPD
    e_data.grid(row=3, column=1, columnspan=2, sticky="w", pady=2)

    tk.Label(form, text="Email:").grid(row=4, column=0, sticky="w")
    e_email = tk.Entry(form, width=30)
    e_email.grid(row=4, column=1, columnspan=2, sticky="w", pady=2)

    tk.Label(form, text="Telefone:").grid(row=5, column=0, sticky="w")
    e_telefone = tk.Entry(form, width=30)
    e_telefone.grid(row=5, column=1, columnspan=2, sticky="w", pady=2)

    tk.Label(form, text="Morada:").grid(row=6, column=0, sticky="w")
    e_morada = tk.Entry(form, width=30)
    e_morada.grid(row=6, column=1, columnspan=2, sticky="w", pady=2)

    tk.Label(form, text="Encarregado:").grid(row=7, column=0, sticky="w")
    cb_encarregado = ttk.Combobox(form, state="readonly", width=24)
    cb_encarregado.grid(row=7, column=1, sticky="w", pady=2)
    b_novo_enc = tk.Button(form, text="Novo...")
    b_novo_enc.grid(row=7, column=2, padx=3)

    cb_consentimento = tk.Checkbutton(form, text="Encarregado deu consentimento RGPD", variable=consentimento)
    cb_consentimento.grid(row=8, column=0, columnspan=3, sticky="w")

    tk.Label(form, text=AVISO_RGPD, fg="red", wraplength=330, justify="left").grid(
        row=9, column=0, columnspan=3, sticky="w", pady=8)

    botoes = tk.Frame(form)
    botoes.grid(row=10, column=0, columnspan=3, pady=5)

    # ----- lista de alunos (lado esquerdo)
    esq = tk.LabelFrame(jan, text="Alunos", padx=5, pady=5)
    esq.pack(side="left", fill="both", expand=True, padx=8, pady=8)

    tk.Label(esq, text="Pesquisar (nome ou NIF):").pack(anchor="w")
    e_pesquisa = tk.Entry(esq, width=30)
    e_pesquisa.pack(anchor="w")

    lista = criar_lista(esq)

    campos = [e_nome, e_apelido, e_nif, e_data, e_email, e_telefone, e_morada]

    # ----- funções da janela
    def carregar_alunos():
        alunos.clear()
        for a in aluno_service.pesquisar(e_pesquisa.get()):
            alunos.append(a)
        lista.delete(0, tk.END)
        for a in alunos:
            texto = str(a._id) + " - " + a._nome + " | " + a._email
            if ver_dados.get():      # só mostra NIF e data com autorização RGPD
                texto = texto + " | NIF " + a._nif + " | nasc. " + a._dataNasc.strftime("%d-%m-%Y")
            if not a._ativo:
                texto = texto + " (arquivado)"
            lista.insert(tk.END, texto)

    def carregar_encarregados():
        encarregados.clear()
        nomes = ["(nenhum)"]
        for enc in listar_encarregados():
            encarregados.append(enc)
            nomes.append(str(enc._id) + " - " + enc._nome)
        cb_encarregado["values"] = nomes
        cb_encarregado.current(0)

    def mudar_rgpd():
        if ver_dados.get():
            e_data.config(show="")
        else:
            e_data.config(show="*")
        carregar_alunos()

    def ativar_formulario(ativo):
        if ativo:
            estado = "normal"
        else:
            estado = "disabled"
        for campo in campos:
            campo.config(state=estado)
        cb_consentimento.config(state=estado)
        b_novo_enc.config(state=estado)
        b_guardar.config(state=estado)
        if ativo:
            cb_encarregado.config(state="readonly")
        else:
            cb_encarregado.config(state="disabled")

    def limpar():
        for campo in campos:
            campo.delete(0, tk.END)
        cb_encarregado.current(0)
        consentimento.set(False)

    def novo_aluno():
        lista.selection_clear(0, tk.END)
        ativar_formulario(True)
        limpar()
        e_nome.focus()

    def mostrar_aluno(evento):
        if not lista.curselection():
            return
        a = alunos[lista.curselection()[0]]
        ativar_formulario(True)
        limpar()
        e_nome.insert(0, a._nome)
        e_nif.insert(0, a._nif)
        e_data.insert(0, str(a._dataNasc))
        e_email.insert(0, a._email)
        e_telefone.insert(0, a._telefone)
        e_morada.insert(0, a._morada)
        consentimento.set(a._consentimentoRGPD)
        ativar_formulario(False)

    def guardar():
        nome = (e_nome.get().strip() + " " + e_apelido.get().strip()).strip()
        email = e_email.get().strip()
        telefone = e_telefone.get().strip()

        try:
            data_nasc = date.fromisoformat(e_data.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Data de nascimento inválida (AAAA-MM-DD).", parent=jan)
            return

        # validar email e telefone antes de chamar o service
        if not email_valido(email):
            messagebox.showerror("Erro", "Email inválido.", parent=jan)
            return
        if not telefone_valido(telefone):
            messagebox.showerror("Erro", "Telefone inválido (9 dígitos, começa por 9 ou 2).", parent=jan)
            return

        # confirmar porque podem ser dados de menores
        if e_menor(data_nasc):
            pergunta = AVISO_RGPD + "\n\nO aluno é menor. Tem autorização do encarregado de educação?"
        else:
            pergunta = "Confirma o registo deste aluno?"
        if not messagebox.askyesno("Confirmar (RGPD)", pergunta, parent=jan):
            return

        aluno = Aluno(0, nome, e_nif.get().strip(), data_nasc, telefone, email, e_morada.get().strip())
        posicao = cb_encarregado.current()
        if posicao > 0:          # a posição 0 é "(nenhum)"
            aluno._id_encarregado = encarregados[posicao - 1]
            aluno._consentimentoRGPD = consentimento.get()

        try:
            novo_id = aluno_service.registar(aluno)
        except ValueError as erro:          # erros das regras do service
            messagebox.showerror("Erro", str(erro), parent=jan)
            return
        except Exception:                   # por exemplo NIF repetido na base de dados
            messagebox.showerror("Erro", "Não foi possível guardar. O NIF já existe?", parent=jan)
            return

        messagebox.showinfo("OK", "Aluno registado com o id " + str(novo_id), parent=jan)
        limpar()
        ativar_formulario(False)
        carregar_alunos()

    def arquivar():
        if not lista.curselection():
            messagebox.showwarning("Aviso", "Escolha um aluno da lista.", parent=jan)
            return
        a = alunos[lista.curselection()[0]]
        if messagebox.askyesno("Arquivar", "Arquivar o aluno " + a._nome + "?", parent=jan):
            aluno_service.arquivar(a._id)
            carregar_alunos()

    def novo_encarregado():
        jan_enc = tk.Toplevel(jan)
        jan_enc.title("Novo encarregado")

        tk.Label(jan_enc, text="Nome:").grid(row=0, column=0, sticky="w", padx=5)
        en_nome = tk.Entry(jan_enc, width=28)
        en_nome.grid(row=0, column=1, pady=2)
        tk.Label(jan_enc, text="NIF:").grid(row=1, column=0, sticky="w", padx=5)
        en_nif = tk.Entry(jan_enc, width=28)
        en_nif.grid(row=1, column=1, pady=2)
        tk.Label(jan_enc, text="Telefone:").grid(row=2, column=0, sticky="w", padx=5)
        en_tel = tk.Entry(jan_enc, width=28)
        en_tel.grid(row=2, column=1, pady=2)
        tk.Label(jan_enc, text="Email:").grid(row=3, column=0, sticky="w", padx=5)
        en_email = tk.Entry(jan_enc, width=28)
        en_email.grid(row=3, column=1, pady=2)
        tk.Label(jan_enc, text="Parentesco:").grid(row=4, column=0, sticky="w", padx=5)
        en_par = tk.Entry(jan_enc, width=28)
        en_par.grid(row=4, column=1, pady=2)

        def guardar_encarregado():
            if en_nome.get().strip() == "":
                messagebox.showerror("Erro", "O nome é obrigatório.", parent=jan_enc)
                return
            enc = EncarregadoEducacao(0, en_nome.get().strip(), en_nif.get().strip(),
                                      en_tel.get().strip(), en_email.get().strip(), en_par.get().strip())
            encarregado_repo.inserir(enc)
            carregar_encarregados()
            cb_encarregado.set(str(enc._id) + " - " + enc._nome)
            jan_enc.destroy()

        tk.Button(jan_enc, text="Guardar", command=guardar_encarregado).grid(row=5, column=1, pady=8)

    # ----- botões e eventos
    tk.Button(botoes, text="Novo Aluno", width=11, command=novo_aluno).pack(side="left", padx=2)
    b_guardar = tk.Button(botoes, text="Guardar", width=11, command=guardar)
    b_guardar.pack(side="left", padx=2)
    tk.Button(botoes, text="Arquivar", width=11, command=arquivar).pack(side="left", padx=2)
    b_novo_enc.config(command=novo_encarregado)

    tk.Button(esq, text="Procurar", command=carregar_alunos).pack(anchor="w")
    tk.Checkbutton(esq, text="Autorizar visualização de dados (RGPD)",
                   variable=ver_dados, command=mudar_rgpd).pack(anchor="w")
    lista.bind("<<ListboxSelect>>", mostrar_aluno)

    ativar_formulario(False)     # só fica ativo com o botão Novo Aluno
    carregar_encarregados()
    carregar_alunos()


# ---------------- T2.4 Gerir Matrículas ----------------

def gerir_matriculas(janela_pai):
    jan = tk.Toplevel(janela_pai)
    jan.title("Gerir Matrículas")
    jan.geometry("560x480")

    alunos = []
    for a in aluno_service.listar():
        if a._ativo:
            alunos.append(a)
    turmas = []
    for t in turma_service.listar():
        if t._ativa:
            turmas.append(t)
    matriculas = []

    form = tk.LabelFrame(jan, text="Nova matrícula", padx=8, pady=8)
    form.pack(fill="x", padx=8, pady=8)

    nomes_alunos = []
    for a in alunos:
        nomes_alunos.append(str(a._id) + " - " + a._nome)
    nomes_turmas = []
    for t in turmas:
        nomes_turmas.append(texto_turma(t))

    tk.Label(form, text="Aluno:").grid(row=0, column=0, sticky="w")
    cb_aluno = ttk.Combobox(form, state="readonly", width=45, values=nomes_alunos)
    cb_aluno.grid(row=0, column=1, pady=3)

    tk.Label(form, text="Turma:").grid(row=1, column=0, sticky="w")
    cb_turma = ttk.Combobox(form, state="readonly", width=45, values=nomes_turmas)
    cb_turma.grid(row=1, column=1, pady=3)

    l_info = tk.Label(form, text="Idioma: -   Nível: -   Vagas: -", fg="blue")
    l_info.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

    tk.Label(form, text="Propina (€):").grid(row=3, column=0, sticky="w")
    e_propina = tk.Entry(form, width=12)
    e_propina.insert(0, "0")
    e_propina.grid(row=3, column=1, sticky="w")

    quadro = tk.LabelFrame(jan, text="Matrículas do aluno", padx=5, pady=5)
    quadro.pack(fill="both", expand=True, padx=8, pady=8)
    lista = criar_lista(quadro)

    def mostrar_turma(evento=None):
        if cb_turma.current() < 0:
            return
        t = turmas[cb_turma.current()]
        idioma = "?"
        nivel = "?"
        if t._idioma:
            idioma = t._idioma._nome
        if t._nivel:
            nivel = t._nivel._codigo
        vagas = turma_service.vagas_disponiveis(t._id)
        l_info.config(text="Idioma: " + idioma + "   Nível: " + nivel +
                      "   Vagas: " + str(vagas) + "/" + str(t._maxAlunos))

    def carregar_matriculas(evento=None):
        lista.delete(0, tk.END)
        matriculas.clear()
        if cb_aluno.current() < 0:
            return
        a = alunos[cb_aluno.current()]
        for m in aluno_service.obter_historico(a._id):
            matriculas.append(m)
            lista.insert(tk.END, "Matrícula " + str(m._id) + " | " + m._dataMatricula.strftime("%d-%m-%Y")
                         + " | " + m._estado + " | " + str(m._valorPropina) + " €")

    def matricular():
        if cb_aluno.current() < 0 or cb_turma.current() < 0:
            messagebox.showwarning("Aviso", "Escolha o aluno e a turma.", parent=jan)
            return
        try:
            propina = float(e_propina.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Valor da propina inválido.", parent=jan)
            return
        m = Matricula(0, date.today(), propina)
        m._aluno = alunos[cb_aluno.current()]
        m._turma = turmas[cb_turma.current()]
        try:
            novo_id = matricula_service.matricular(m)    # o service verifica as vagas
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro), parent=jan)
            return
        except Exception:
            messagebox.showerror("Erro", "O aluno já está matriculado nesta turma.", parent=jan)
            return
        messagebox.showinfo("OK", "Matrícula criada com o id " + str(novo_id), parent=jan)
        mostrar_turma()
        carregar_matriculas()

    def cancelar():
        if not lista.curselection():
            messagebox.showwarning("Aviso", "Escolha uma matrícula da lista.", parent=jan)
            return
        m = matriculas[lista.curselection()[0]]
        if m._estado != "ativa":
            messagebox.showinfo("Aviso", "Esta matrícula já não está ativa.", parent=jan)
            return
        if messagebox.askyesno("Cancelar", "Cancelar a matrícula " + str(m._id) + "?", parent=jan):
            matricula_service.cancelar(m._id)
            mostrar_turma()
            carregar_matriculas()

    tk.Button(form, text="Matricular", width=15, command=matricular).grid(row=4, column=1, sticky="e", pady=5)
    tk.Button(quadro, text="Cancelar matrícula", command=cancelar).pack(anchor="e")
    cb_turma.bind("<<ComboboxSelected>>", mostrar_turma)
    cb_aluno.bind("<<ComboboxSelected>>", carregar_matriculas)


# ---------------- T2.5 Gerir Idiomas ----------------

def gerir_idiomas(janela_pai):
    jan = tk.Toplevel(janela_pai)
    jan.title("Gerir Idiomas")
    jan.geometry("420x400")

    quadro = tk.LabelFrame(jan, text="Idiomas", padx=5, pady=5)
    quadro.pack(fill="both", expand=True, padx=8, pady=8)
    lista = criar_lista(quadro)

    form = tk.Frame(quadro)
    form.pack(fill="x", pady=5)
    tk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w")
    e_nome = tk.Entry(form, width=20)
    e_nome.grid(row=0, column=1, padx=4)
    tk.Label(form, text="Código:").grid(row=1, column=0, sticky="w")
    e_codigo = tk.Entry(form, width=8)
    e_codigo.grid(row=1, column=1, padx=4, sticky="w")

    def carregar():
        lista.delete(0, tk.END)
        for i in idioma_service.listar():
            lista.insert(tk.END, i._codigo + " - " + i._nome)

    def adicionar():
        idioma = Idioma(0, e_nome.get().strip(), e_codigo.get().strip().upper())
        try:
            idioma_service.registar(idioma)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro), parent=jan)
            return
        e_nome.delete(0, tk.END)
        e_codigo.delete(0, tk.END)
        carregar()

    def remover():
        # o idioma_service não tem eliminar e não podemos alterar os services
        if not lista.curselection():
            messagebox.showwarning("Aviso", "Escolha um idioma da lista.", parent=jan)
            return
        messagebox.showinfo("Remover", "Remover idiomas ainda não está disponível no serviço.", parent=jan)

    tk.Button(form, text="Adicionar", width=10, command=adicionar).grid(row=0, column=2, padx=4)
    tk.Button(form, text="Remover", width=10, command=remover).grid(row=1, column=2)
    carregar()


# ---------------- T2.5 Gerir Níveis ----------------

def gerir_niveis(janela_pai):
    jan = tk.Toplevel(janela_pai)
    jan.title("Gerir Níveis")
    jan.geometry("460x430")

    quadro = tk.LabelFrame(jan, text="Níveis", padx=5, pady=5)
    quadro.pack(fill="both", expand=True, padx=8, pady=8)
    lista = criar_lista(quadro)

    form = tk.Frame(quadro)
    form.pack(fill="x", pady=5)
    tk.Label(form, text="Designação:").grid(row=0, column=0, sticky="w")
    cb_codigo = ttk.Combobox(form, state="readonly", width=6, values=["A1", "A2", "B1", "B2", "C1", "C2"])
    cb_codigo.grid(row=0, column=1, sticky="w", padx=4)
    tk.Label(form, text="Descrição:").grid(row=1, column=0, sticky="w")
    e_descricao = tk.Entry(form, width=25)
    e_descricao.grid(row=1, column=1, columnspan=3, sticky="w", padx=4)

    # ponderações da nota final (têm de somar 1)
    tk.Label(form, text="Oral").grid(row=2, column=0)
    tk.Label(form, text="Escrito").grid(row=2, column=1)
    tk.Label(form, text="Projeto").grid(row=2, column=2)
    e_oral = tk.Entry(form, width=6)
    e_oral.insert(0, "0.3")
    e_oral.grid(row=3, column=0)
    e_escrito = tk.Entry(form, width=6)
    e_escrito.insert(0, "0.4")
    e_escrito.grid(row=3, column=1)
    e_projeto = tk.Entry(form, width=6)
    e_projeto.insert(0, "0.3")
    e_projeto.grid(row=3, column=2)

    def carregar():
        lista.delete(0, tk.END)
        for n in nivel_service.listar():
            lista.insert(tk.END, n._codigo + " - " + n._descricao + " (oral " + str(n._pondOral) +
                         ", escrito " + str(n._pondEscrito) + ", projeto " + str(n._pondProjeto) + ")")

    def adicionar():
        try:
            oral = float(e_oral.get())
            escrito = float(e_escrito.get())
            projeto = float(e_projeto.get())
        except ValueError:
            messagebox.showerror("Erro", "As ponderações têm de ser números (ex: 0.3).", parent=jan)
            return
        nivel = Nivel(0, cb_codigo.get(), e_descricao.get().strip(), oral, escrito, projeto)
        try:
            nivel_service.registar(nivel)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro), parent=jan)
            return
        e_descricao.delete(0, tk.END)
        carregar()

    def remover():
        # o nivel_service não tem eliminar e não podemos alterar os services
        if not lista.curselection():
            messagebox.showwarning("Aviso", "Escolha um nível da lista.", parent=jan)
            return
        messagebox.showinfo("Remover", "Remover níveis ainda não está disponível no serviço.", parent=jan)

    botoes = tk.Frame(quadro)
    botoes.pack(fill="x")
    tk.Button(botoes, text="Adicionar", width=10, command=adicionar).pack(side="left", padx=4)
    tk.Button(botoes, text="Remover", width=10, command=remover).pack(side="left")
    carregar()


# para testar só este menu: python src/views/menu_secretaria_gui.py
if __name__ == "__main__":
    inicializar_bd()
    janela = tk.Tk()
    abrir_menu_secretaria(janela)
    janela.mainloop()