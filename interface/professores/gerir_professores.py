
import tkinter as tk
from tkinter import ttk, messagebox

from services.professor_service import ProfessorService
from services.idioma_service import IdiomaService
from models.professor import Professor


def criar_janela_professores(janela_pai):

    professor_service = ProfessorService()
    idioma_service = IdiomaService()

    janela = tk.Toplevel(janela_pai)
    janela.title("LinguaViva - Gerir Professores")
    janela.geometry("900x650")
    janela.resizable(False, False)

    professor_selecionado = None
    professores_lista = []
    idiomas_mapa = {}

    frame = ttk.LabelFrame(
        janela,
        text="Gerir Professores",
        padding=15
    )
    frame.pack(
        padx=15,
        pady=15,
        fill="both",
        expand=True
    )

    frame_lista = ttk.LabelFrame(
        frame,
        text="Professores registados",
        padding=10
    )

    frame_lista.place(x=10, y=10, width=300, height=520)

    frame_formulario = ttk.LabelFrame(
        frame,
        text="Dados do Professor",
        padding=15
    )
    frame_formulario.place(x=325, y=10, width=450, height=520)

    lista_professores = tk.Listbox(
        frame_lista,
        width=35,
        height=23,
        exportselection=False
    )
    lista_professores.pack(
        fill="both",
        expand=True
    )

    ttk.Label(frame_formulario, text="Nome:").pack(anchor="w", pady=3)

    entrada_nome = ttk.Entry(frame_formulario, width=45)
    entrada_nome.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Email:").pack(anchor="w", pady=3)

    entrada_email = ttk.Entry(frame_formulario, width=45)
    entrada_email.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Telefone:").pack(anchor="w", pady=3)

    entrada_telefone = ttk.Entry(frame_formulario, width=45)
    entrada_telefone.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Custo por hora (€):").pack(
        anchor="w", pady=3
    )

    entrada_custo = ttk.Entry(frame_formulario, width=45)
    entrada_custo.pack(fill="x", pady=3)

    ttk.Label(frame_formulario, text="Especialidade:").pack(
        anchor="w", pady=3
    )

    ttk.Label(
        frame_formulario,
        text="Especialidades (pode selecionar vários):"
    ).pack(anchor="w", pady=3)

    lista_idiomas = tk.Listbox(
        frame_formulario,
        selectmode=tk.MULTIPLE,
        exportselection=False,
        height=5,
        width=42
    )

    lista_idiomas.pack(fill="x", pady=3)

    frame_botoes = ttk.Frame(frame_formulario)
    frame_botoes.pack(fill="x", pady=15)

    def carregar_idiomas():

        lista_idiomas.delete(0, tk.END)

        idiomas = idioma_service.listar()

        for idioma in idiomas:
            lista_idiomas.insert(
                tk.END,
                f"{idioma._nome} ({idioma._codigo})"
            )

    def limpar():

        nonlocal professor_selecionado

        professor_selecionado = None

        entrada_nome.delete(0, tk.END)
        entrada_email.delete(0, tk.END)
        entrada_telefone.delete(0, tk.END)
        entrada_custo.delete(0, tk.END)

        lista_idiomas.selection_clear(0, tk.END)

        lista_professores.selection_clear(0, tk.END)

    def carregar_professores():

        nonlocal professores_lista

        lista_professores.delete(0, tk.END)

        professores_lista = [
            p for p in professor_service.listar()
            if p._ativo
        ]

        for professor in professores_lista:
            lista_professores.insert(
                tk.END,
                professor._nome
            )

    def selecionar_professor(event):

        nonlocal professor_selecionado

        selecao = lista_professores.curselection()

        if not selecao:
            return

        indice = selecao[0]

        professor = professores_lista[indice]

        professor_selecionado = professor._id

        entrada_nome.delete(0, tk.END)
        entrada_nome.insert(0, professor._nome)

        entrada_email.delete(0, tk.END)
        entrada_email.insert(0, professor._email)

        entrada_telefone.delete(0, tk.END)
        entrada_telefone.insert(0, professor._telefone)

        entrada_custo.delete(0, tk.END)
        entrada_custo.insert(0, str(professor._custoHora))

        idiomas_ids = professor_service.listar_idiomas(
            professor._id
        )

        lista_idiomas.selection_clear(0, tk.END)

        idiomas_disponiveis = idioma_service.listar()

        for indice, idioma in enumerate(idiomas_disponiveis):

            if idioma._id in idiomas_ids:
                lista_idiomas.selection_set(indice)

    def obter_dados():

        nome = entrada_nome.get().strip()
        email = entrada_email.get().strip()
        telefone = entrada_telefone.get().strip()
        custo_texto = entrada_custo.get().strip().replace(",", ".")

        if not nome:
            raise ValueError("O nome é obrigatório.")

        try:
            custo = float(custo_texto or "0")
        except ValueError:
            raise ValueError("O custo por hora deve ser numérico.")

        if custo < 0:
            raise ValueError("O custo por hora não pode ser negativo.")

        idiomas_disponiveis = idioma_service.listar()

        indices = lista_idiomas.curselection()

        idiomas_ids = [
            idiomas_disponiveis[indice]._id
            for indice in indices
        ]

        if not idiomas_ids:
            raise ValueError("Selecione pelo menos um idioma.")

        return nome, email, telefone, custo, idiomas_ids

    def adicionar():
        try:
            nome, email, telefone, custo, idioma_ids = obter_dados()

            professor = Professor(
                id=0,
                nome=nome,
                telefone=telefone,
                email=email,
                custoHora=custo
            )

            professor_service.registar(
                professor,
                idioma_ids
            )

            messagebox.showinfo(
                "Sucesso",
                "Professor registado com sucesso!"
            )

            carregar_professores()
            limpar()

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível registar:\n{erro}")

    def editar():

        if professor_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione um professor para editar."
            )
            return

        try:
            nome, email, telefone, custo, idioma_ids = obter_dados()

            professor = Professor(
                id=professor_selecionado,
                nome=nome,
                telefone=telefone,
                email=email,
                custoHora=custo
            )

            professor_service.atualizar(
                professor,
                idioma_ids
            )

            messagebox.showinfo(
                "Sucesso",
                "Professor atualizado com sucesso!"
            )

            carregar_professores()
            limpar()

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível editar:\n{erro}")

    def desativar():

        if professor_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione um professor para desativar."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Tem a certeza de que pretende desativar este professor?"
        )

        if not confirmar:
            return

        try:
            professor_service.desativar(professor_selecionado)

            messagebox.showinfo(
                "Sucesso",
                "Professor desativado com sucesso!"
            )

            carregar_professores()
            limpar()

        except ValueError as erro:
            messagebox.showerror("Não foi possível desativar", str(erro))

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

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

    lista_professores.bind(
        "<<ListboxSelect>>",
        selecionar_professor
    )

    carregar_idiomas()
    carregar_professores()
