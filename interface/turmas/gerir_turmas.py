
import tkinter as tk
from tkinter import ttk, messagebox

from services.turma_service import TurmaService
from services.professor_service import ProfessorService
from services.idioma_service import IdiomaService
from services.nivel_service import NivelService

from models.turma import Turma


def criar_janela_turmas(janela_pai):

    turma_service = TurmaService()
    professor_service = ProfessorService()
    idioma_service = IdiomaService()
    nivel_service = NivelService()

    janela = tk.Toplevel(janela_pai)
    janela.title("LinguaViva - Gerir Turmas")
    janela.geometry("1050x700")
    janela.resizable(False, False)

    turma_selecionada = None
    turmas_lista = []

    idiomas_lista = []
    niveis_lista = []
    professores_lista = []

    frame = ttk.LabelFrame(
        janela,
        text="Gestão de Turmas",
        padding=15
    )
    frame.pack(padx=15, pady=15, fill="both", expand=True)

    frame_lista = ttk.LabelFrame(
        frame,
        text="Turmas registadas",
        padding=10
    )
    frame_lista.place(x=10, y=10, width=300, height=560)

    frame_formulario = ttk.LabelFrame(
        frame,
        text="Dados da Turma",
        padding=15
    )
    frame_formulario.place(x=325, y=10, width=650, height=560)

    lista_turmas = tk.Listbox(
        frame_lista,
        width=40,
        height=28,
        exportselection=False
    )
    lista_turmas.pack(fill="both", expand=True)

    ttk.Label(frame_formulario, text="Idioma:").pack(anchor="w", pady=3)

    combo_idioma = ttk.Combobox(
        frame_formulario,
        state="readonly",
        width=55
    )
    combo_idioma.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Nível:").pack(anchor="w", pady=3)

    combo_nivel = ttk.Combobox(
        frame_formulario,
        state="readonly",
        width=55
    )
    combo_nivel.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Professor:").pack(anchor="w", pady=3)

    combo_professor = ttk.Combobox(
        frame_formulario,
        state="readonly",
        width=55
    )
    combo_professor.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Horário:").pack(anchor="w", pady=3)

    entrada_horario = ttk.Entry(frame_formulario)
    entrada_horario.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Sala:").pack(anchor="w", pady=3)

    entrada_sala = ttk.Entry(frame_formulario)
    entrada_sala.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Máximo de alunos (6 a 12):").pack(
        anchor="w", pady=3
    )

    entrada_max_alunos = ttk.Entry(frame_formulario)
    entrada_max_alunos.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Semestre:").pack(anchor="w", pady=3)

    combo_semestre = ttk.Combobox(
        frame_formulario,
        values=["1", "2"],
        state="readonly"
    )
    combo_semestre.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Ano:").pack(anchor="w", pady=3)

    entrada_ano = ttk.Entry(frame_formulario)
    entrada_ano.pack(fill="x", pady=3)

    def carregar_combos():

        nonlocal idiomas_lista, niveis_lista, professores_lista

        idiomas_lista = idioma_service.listar()
        niveis_lista = nivel_service.listar()

        professores_lista = [
            p for p in professor_service.listar()
            if p._ativo
        ]

        combo_idioma["values"] = [
            f"{i._nome} ({i._codigo})"
            for i in idiomas_lista
        ]

        combo_nivel["values"] = [
            f"{n._codigo} - {n._descricao}"
            for n in niveis_lista
        ]

        combo_professor["values"] = [
            p._nome for p in professores_lista
        ]

    def limpar():

        nonlocal turma_selecionada

        turma_selecionada = None

        combo_idioma.set("")
        combo_nivel.set("")
        combo_professor.set("")
        combo_semestre.set("")

        entrada_horario.delete(0, tk.END)
        entrada_sala.delete(0, tk.END)
        entrada_max_alunos.delete(0, tk.END)
        entrada_ano.delete(0, tk.END)

        lista_turmas.selection_clear(0, tk.END)


    def carregar_turmas():

        nonlocal turmas_lista

        lista_turmas.delete(0, tk.END)

        turmas_lista = [
            t for t in turma_service.listar()
            if t._ativa
        ]

        for turma in turmas_lista:

            idioma = turma._idioma._nome if turma._idioma else "Sem idioma"
            nivel = turma._nivel._codigo if turma._nivel else "Sem nível"

            lista_turmas.insert(
                tk.END,
                f"{idioma} - {nivel} | {turma._ano}"
            )

    def selecionar_turma(event):

        nonlocal turma_selecionada

        selecao = lista_turmas.curselection()

        if not selecao:
            return

        indice = selecao[0]
        turma = turmas_lista[indice]

        turma_selecionada = turma._id

        for i, idioma in enumerate(idiomas_lista):
            if turma._idioma and idioma._id == turma._idioma._id:
                combo_idioma.current(i)
                break

        for i, nivel in enumerate(niveis_lista):
            if turma._nivel and nivel._id == turma._nivel._id:
                combo_nivel.current(i)
                break

        for i, professor in enumerate(professores_lista):
            if turma._professor and professor._id == turma._professor._id:
                combo_professor.current(i)
                break

        entrada_horario.delete(0, tk.END)
        entrada_horario.insert(0, turma._horario)

        entrada_sala.delete(0, tk.END)
        entrada_sala.insert(0, turma._sala)

        entrada_max_alunos.delete(0, tk.END)
        entrada_max_alunos.insert(0, str(turma._maxAlunos))

        combo_semestre.set(str(turma._semestre))

        entrada_ano.delete(0, tk.END)
        entrada_ano.insert(0, str(turma._ano))

    def obter_dados():

        indice_idioma = combo_idioma.current()
        indice_nivel = combo_nivel.current()
        indice_professor = combo_professor.current()

        if indice_idioma < 0:
            raise ValueError("Selecione um idioma.")

        if indice_nivel < 0:
            raise ValueError("Selecione um nível.")

        if indice_professor < 0:
            raise ValueError("Selecione um professor.")

        horario = entrada_horario.get().strip()
        sala = entrada_sala.get().strip()
        max_alunos_texto = entrada_max_alunos.get().strip()
        semestre_texto = combo_semestre.get()
        ano_texto = entrada_ano.get().strip()

        if not horario:
            raise ValueError("O horário é obrigatório.")

        if not sala:
            raise ValueError("A sala é obrigatória.")

        try:
            max_alunos = int(max_alunos_texto)
            semestre = int(semestre_texto)
            ano = int(ano_texto)
        except ValueError:
            raise ValueError("Verifique o número de alunos, semestre e ano.")

        if not (6 <= max_alunos <= 12):
            raise ValueError("O máximo de alunos tem de estar entre 6 e 12.")

        if semestre not in (1, 2):
            raise ValueError("O semestre tem de ser 1 ou 2.")

        if ano <= 0:
            raise ValueError("O ano tem de ser válido.")

        return (
            idiomas_lista[indice_idioma],
            niveis_lista[indice_nivel],
            professores_lista[indice_professor],
            horario,
            sala,
            max_alunos,
            semestre,
            ano
        )


    def adicionar():

        try:

            dados = obter_dados()

            idioma, nivel, professor, horario, sala, max_alunos, semestre, ano = dados

            turma = Turma(
                id=0,
                horario=horario,
                sala=sala,
                maxAlunos=max_alunos,
                semestre=semestre,
                ano=ano
            )

            turma._idioma = idioma
            turma._nivel = nivel
            turma._professor = professor

            turma_service.criar(turma)

            messagebox.showinfo(
                "Sucesso",
                "Turma criada com sucesso!"
            )

            carregar_turmas()
            limpar()

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível criar a turma:\n{erro}"
            )


    def editar():

        if turma_selecionada is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione uma turma para editar."
            )
            return

        try:

            dados = obter_dados()

            idioma, nivel, professor, horario, sala, max_alunos, semestre, ano = dados

            turma = Turma(
                id=turma_selecionada,
                horario=horario,
                sala=sala,
                maxAlunos=max_alunos,
                semestre=semestre,
                ano=ano
            )

            turma._idioma = idioma
            turma._nivel = nivel
            turma._professor = professor

            turma_service.atualizar(turma)

            messagebox.showinfo(
                "Sucesso",
                "Turma atualizada com sucesso!"
            )

            carregar_turmas()
            limpar()

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível editar a turma:\n{erro}"
            )


    def desativar():

        if turma_selecionada is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione uma turma para desativar."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Tem a certeza de que pretende desativar esta turma?"
        )

        if not confirmar:
            return

        try:

            turma_service.desativar(turma_selecionada)

            messagebox.showinfo(
                "Sucesso",
                "Turma desativada com sucesso!"
            )

            carregar_turmas()
            limpar()

        except ValueError as erro:
            messagebox.showerror("Não foi possível desativar", str(erro))

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    frame_botoes = ttk.Frame(frame_formulario)
    frame_botoes.pack(fill="x", pady=15)

    ttk.Button(
        frame_botoes,
        text="Adicionar",
        command=adicionar
    ).pack(side="left", expand=True, fill="x", padx=3)

    ttk.Button(
        frame_botoes,
        text="Editar",
        command=editar
    ).pack(side="left", expand=True, fill="x", padx=3)

    ttk.Button(
        frame_botoes,
        text="Desativar",
        command=desativar
    ).pack(side="left", expand=True, fill="x", padx=3)

    ttk.Button(
        frame_botoes,
        text="Limpar",
        command=limpar
    ).pack(side="left", expand=True, fill="x", padx=3)

    lista_turmas.bind(
        "<<ListboxSelect>>",
        selecionar_turma
    )

    carregar_combos()
    carregar_turmas()
