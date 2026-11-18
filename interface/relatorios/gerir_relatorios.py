
import tkinter as tk
from tkinter import ttk, messagebox

from services.aluno_service import AlunoService
from services.professor_service import ProfessorService
from services.turma_service import TurmaService


def criar_janela_relatorios(janela):

    janela_relatorios = tk.Toplevel(janela)
    janela_relatorios.title("LinguaViva - Relatórios")
    janela_relatorios.geometry("500x400")
    janela_relatorios.resizable(False, False)

    aluno_service = AlunoService()
    professor_service = ProfessorService()
    turma_service = TurmaService()

    frame = ttk.LabelFrame(
        janela_relatorios,
        text="Relatórios Gerais",
        padding=25
    )
    frame.pack(padx=30, pady=30, fill="both", expand=True)

    ttk.Label(
        frame,
        text="Indicadores da Escola",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    label_alunos = ttk.Label(
        frame,
        text="Total de Alunos: 0",
        font=("Arial", 12)
    )
    label_alunos.pack(pady=10)

    label_professores = ttk.Label(
        frame,
        text="Total de Professores: 0",
        font=("Arial", 12)
    )
    label_professores.pack(pady=10)

    label_turmas = ttk.Label(
        frame,
        text="Turmas Ativas: 0",
        font=("Arial", 12)
    )
    label_turmas.pack(pady=10)

    def atualizar():

        try:
            alunos = aluno_service.listar()
            professores = professor_service.listar()
            turmas = turma_service.listar()

            total_alunos = len(alunos)
            total_professores = len(professores)
            total_turmas_ativas = sum(
                1 for turma in turmas if turma._ativa
            )

            label_alunos.config(
                text=f"Total de Alunos: {total_alunos}"
            )

            label_professores.config(
                text=f"Total de Professores: {total_professores}"
            )

            label_turmas.config(
                text=f"Turmas Ativas: {total_turmas_ativas}"
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível atualizar os relatórios:\n{erro}"
            )

    ttk.Button(
        frame,
        text="Atualizar",
        command=atualizar,
        width=25
    ).pack(pady=25, ipady=5)

    atualizar()
