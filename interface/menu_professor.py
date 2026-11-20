import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox

from interface.rgpd_panel import RGPDPanel
from models.aula import Aula
from models.avaliacao import Avaliacao
from models.presenca import Presenca
from repositories.matricula_repository import MatriculaRepository
from services.aula_service import AulaService
from services.matricula_service import MatriculaService
from services.professor_service import ProfessorService
from services.turma_service import TurmaService


class MenuProfessorGUI:
    def __init__(self, root, rgpd_validado=False):
        self.root = root
        self.root.title("LinguaViva - Menu Professor")
        self.root.geometry("500x650")
        self.rgpd_validado = rgpd_validado
        self.professor_service = ProfessorService()
        self.turma_service = TurmaService()
        self.aula_service = AulaService()
        self.matricula_service = MatriculaService()
        self.matricula_repo = MatriculaRepository()
        self.professores = [p for p in self.professor_service.listar() if p._ativo]
        self.professor_atual = None

        self.main_frame = ttk.LabelFrame(root, text="Menu - Professor")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        ttk.Label(self.main_frame, text="Professor:").pack(anchor="w", padx=10, pady=(10, 0))
        self.combo_professor = ttk.Combobox(
            self.main_frame, state="readonly",
            values=[f"{p._id} - {p._nome}" for p in self.professores],
        )
        self.combo_professor.pack(fill="x", padx=10, pady=5)
        self.combo_professor.bind("<<ComboboxSelected>>", self.selecionar_professor)

        self.rgpd_panel = RGPDPanel(self.main_frame, self.atualizar_rgpd)
        self.rgpd_panel.pack(fill="x", padx=10, pady=10)
        self.rgpd_panel.var_confirmacao.set(rgpd_validado)

        for texto, comando in (
            ("Registar Aula", self.abrir_registar_aula),
            ("Registar Presenças", self.abrir_registar_presencas),
            ("Registar Avaliação", self.abrir_avaliacoes),
            ("As Minhas Turmas", self.abrir_minhas_turmas),
            ("Voltar", root.destroy),
        ):
            ttk.Button(self.main_frame, text=texto, command=comando).pack(
                fill="x", padx=10, pady=5 if texto != "Voltar" else 15
            )

    def atualizar_rgpd(self, confirmado):
        self.rgpd_validado = confirmado

    def selecionar_professor(self, evento=None):
        indice = self.combo_professor.current()
        self.professor_atual = self.professores[indice] if indice >= 0 else None

    def verificar_rgpd(self):
        if not self.rgpd_validado:
            messagebox.showwarning("Aviso RGPD", "Necessário confirmar a autorização no Painel RGPD para aceder a dados de alunos.")
            return False
        if self.professor_atual is None:
            messagebox.showwarning("Professor", "Selecione o professor que está a utilizar a aplicação.")
            return False
        return True

    def minhas_turmas(self):
        if self.professor_atual is None:
            return []
        return [turma for turma in self.turma_service.listar()
                if turma._ativa and turma._professor and turma._professor._id == self.professor_atual._id]

    @staticmethod
    def texto_turma(turma):
        idioma = turma._idioma._nome if turma._idioma else "?"
        nivel = turma._nivel._codigo if turma._nivel else "?"
        return f"{turma._id} - {idioma} {nivel} | {turma._horario}"

    def criar_combo_turmas(self, parent):
        turmas = self.minhas_turmas()
        combo = ttk.Combobox(parent, state="readonly", values=[self.texto_turma(t) for t in turmas])
        combo.pack(fill="x", padx=10)
        return combo, turmas

    def abrir_registar_aula(self):
        if not self.verificar_rgpd():
            return
        janela = tk.Toplevel(self.root)
        janela.title("Registar Aula")
        janela.geometry("400x330")
        ttk.Label(janela, text="Turma:").pack(anchor="w", padx=10, pady=5)
        combo_turma, turmas = self.criar_combo_turmas(janela)
        ttk.Label(janela, text="Data (AAAA-MM-DD):").pack(anchor="w", padx=10, pady=5)
        entry_data = ttk.Entry(janela)
        entry_data.insert(0, date.today().isoformat())
        entry_data.pack(fill="x", padx=10)
        ttk.Label(janela, text="Sumário:").pack(anchor="w", padx=10, pady=5)
        text_sumario = tk.Text(janela, height=5)
        text_sumario.pack(fill="x", padx=10)

        def guardar_aula():
            if combo_turma.current() < 0:
                messagebox.showerror("Erro", "Selecione uma turma.", parent=janela)
                return
            try:
                data_aula = date.fromisoformat(entry_data.get().strip())
            except ValueError:
                messagebox.showerror("Erro", "A data deve estar no formato AAAA-MM-DD.", parent=janela)
                return
            aula = Aula(0, data_aula, text_sumario.get("1.0", tk.END).strip())
            aula._turma = turmas[combo_turma.current()]
            aula._professor = self.professor_atual
            try:
                self.aula_service.registar(aula)
            except ValueError as erro:
                messagebox.showerror("Erro", str(erro), parent=janela)
                return
            messagebox.showinfo("Sucesso", "Aula registada com sucesso.", parent=janela)
            janela.destroy()

        ttk.Button(janela, text="Guardar", command=guardar_aula).pack(pady=15)

    def abrir_registar_presencas(self):
        if not self.verificar_rgpd():
            return
        janela = tk.Toplevel(self.root)
        janela.title("Registar Presenças")
        janela.geometry("430x500")
        ttk.Label(janela, text="Turma:").pack(anchor="w", padx=10, pady=5)
        combo_turma, turmas = self.criar_combo_turmas(janela)
        ttk.Label(janela, text="Selecionar Aula:").pack(anchor="w", padx=10, pady=5)
        combo_aula = ttk.Combobox(janela, state="readonly")
        combo_aula.pack(fill="x", padx=10)
        frame_alunos = ttk.LabelFrame(janela, text="Alunos da Turma")
        frame_alunos.pack(fill="both", expand=True, padx=10, pady=10)
        aulas, presencas = [], []

        def carregar_turma(evento=None):
            aulas.clear()
            presencas.clear()
            combo_aula.set("")
            combo_aula["values"] = []
            for widget in frame_alunos.winfo_children():
                widget.destroy()
            if combo_turma.current() < 0:
                return
            turma = turmas[combo_turma.current()]
            aulas.extend(self.aula_service.listar_por_turma(turma._id))
            combo_aula["values"] = [f"{a._id} - {a._data.isoformat()} | {a._sumario}" for a in aulas]
            for matricula in self.matricula_repo.listar_por_turma(turma._id):
                if matricula._estado != "ativa":
                    continue
                var = tk.BooleanVar(value=True)
                ttk.Checkbutton(frame_alunos, text=matricula._aluno._nome, variable=var).pack(anchor="w", padx=5, pady=2)
                presencas.append((matricula, var))

        def guardar_presencas():
            if combo_aula.current() < 0:
                messagebox.showerror("Erro", "Selecione uma aula.", parent=janela)
                return
            registos = []
            for matricula, var in presencas:
                presenca = Presenca(0, "P" if var.get() else "A")
                presenca._matricula = matricula
                registos.append(presenca)
            try:
                self.aula_service.registar_presencas(aulas[combo_aula.current()]._id, registos)
            except Exception as erro:
                messagebox.showerror("Erro", str(erro), parent=janela)
                return
            messagebox.showinfo("Sucesso", "Presenças guardadas com sucesso.", parent=janela)
            janela.destroy()

        combo_turma.bind("<<ComboboxSelected>>", carregar_turma)
        ttk.Button(janela, text="Guardar Presenças", command=guardar_presencas).pack(pady=10)

    def abrir_avaliacoes(self):
        if not self.verificar_rgpd():
            return
        janela = tk.Toplevel(self.root)
        janela.title("Registar Avaliação")
        janela.geometry("400x380")
        ttk.Label(janela, text="Turma:").pack(anchor="w", padx=10, pady=5)
        combo_turma, turmas = self.criar_combo_turmas(janela)
        ttk.Label(janela, text="Aluno:").pack(anchor="w", padx=10, pady=5)
        combo_aluno = ttk.Combobox(janela, state="readonly")
        combo_aluno.pack(fill="x", padx=10)
        ttk.Label(janela, text="Tipo:").pack(anchor="w", padx=10, pady=5)
        combo_tipo = ttk.Combobox(janela, state="readonly", values=("oral", "escrito", "projeto"))
        combo_tipo.pack(fill="x", padx=10)
        ttk.Label(janela, text="Nota (0-20):").pack(anchor="w", padx=10, pady=5)
        entry_nota = ttk.Entry(janela)
        entry_nota.pack(fill="x", padx=10)
        matriculas = []

        def carregar_alunos(evento=None):
            matriculas.clear()
            combo_aluno.set("")
            combo_aluno["values"] = []
            if combo_turma.current() >= 0:
                for matricula in self.matricula_repo.listar_por_turma(turmas[combo_turma.current()]._id):
                    if matricula._estado == "ativa":
                        matriculas.append(matricula)
                combo_aluno["values"] = [m._aluno._nome for m in matriculas]

        def guardar_avaliacao():
            if combo_aluno.current() < 0 or combo_tipo.current() < 0:
                messagebox.showerror("Erro", "Selecione o aluno e o tipo de avaliação.", parent=janela)
                return
            try:
                nota = float(entry_nota.get().replace(",", "."))
                avaliacao = Avaliacao(0, combo_tipo.get(), nota, date.today())
                self.matricula_service.registar_avaliacao(matriculas[combo_aluno.current()]._id, avaliacao)
            except ValueError as erro:
                messagebox.showerror("Erro de Validação", str(erro), parent=janela)
                return
            messagebox.showinfo("Sucesso", "Avaliação registada com sucesso.", parent=janela)
            janela.destroy()

        combo_turma.bind("<<ComboboxSelected>>", carregar_alunos)
        ttk.Button(janela, text="Guardar", command=guardar_avaliacao).pack(pady=15)

    def abrir_minhas_turmas(self):
        if not self.verificar_rgpd():
            return
        janela = tk.Toplevel(self.root)
        janela.title("As Minhas Turmas")
        janela.geometry("400x300")
        listbox = tk.Listbox(janela)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)
        for turma in self.minhas_turmas():
            listbox.insert(tk.END, self.texto_turma(turma))
