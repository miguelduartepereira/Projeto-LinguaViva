# Sistema de Gestão — Centro de Línguas LinguaViva

> UFCD 10790 — Gestão e Planeamento de Projetos de SI · IEFP 2026 · **Grupo 4**

## Introdução

O **LinguaViva** é um centro de línguas em Setúbal com cerca de 300 alunos e 12 professores,
que oferece turmas de inglês, francês, alemão, espanhol, italiano e português para estrangeiros
(níveis A1 a C2 do Quadro Europeu Comum de Referência).

Até agora a gestão era **manual e dispersa**: fichas de alunos em papel, presenças em folhas
impressas, notas em Excel e certificados feitos à mão no Word. No fim de cada semestre, a
secretaria demorava cerca de 3 dias a processar tudo.

Este projeto é um **sistema integrado** que automatiza todo o ciclo de vida do aluno —
matrícula, frequência de aulas, avaliações, cálculo de nota final e assiduidade, e emissão
de certificados — com especial atenção à **proteção de dados de menores (RGPD)**.

## Objetivos

- Centralizar a gestão de alunos, professores, idiomas, níveis e turmas.
- Matricular alunos em turmas com **verificação de vagas**.
- Registar aulas e presenças e calcular a **assiduidade**.
- Registar avaliações (oral/escrito/projeto) e calcular a **nota final ponderada**.
- Emitir **certificados** apenas para alunos aprovados.
- Produzir **relatórios** de assiduidade e de aprovados por turma.

## Funcionalidades principais

| Requisito | Descrição |
|-----------|-----------|
| RF01 | Registo de aluno (menores: dados do encarregado de educação) |
| RF02 | Registo de professor com idiomas que leciona e custo/hora |
| RF03 | Criação de turma (idioma + nível + professor + horário + sala) |
| RF04 | Matrícula com verificação de vaga (turmas de 6 a 12 alunos) |
| RF05/RF06 | Registo de aulas e de presenças (Presente/Ausente/Justificado) |
| RF07 | Cálculo automático da taxa de assiduidade |
| RF08/RF09 | Avaliações (escala 0–20) e nota final = média ponderada por nível |
| RF10 | Certificado apenas com assiduidade ≥ 75% **e** nota final ≥ 10 |
| RF11 | Pesquisa de aluno por nome ou NIF, com acesso ao histórico |
| RF12 | Listagem de turmas com nº de inscritos vs. máximo |
| RF13/RF14 | Relatórios de assiduidade e de aprovados/reprovados por turma |

Regras não-funcionais implementadas: validação de notas (RNF01), nº de certificado único
`ANO-IDIOMA-NIVEL-SEQUENCIAL` (RNF02), perfis de acesso (RNF03), consentimento RGPD para
menores (RNF04), *soft delete* / arquivo em vez de eliminação (RNF07) e integridade
referencial (RNF08).

## Arquitetura

O projeto segue uma **arquitetura em camadas**, em que cada camada só conhece a de baixo:

```
Interface (menu)  ->  Serviços  ->  Repositórios  ->  Base de dados (SQLite)
   main.py           regras de        acesso a           schema.sql
                     negócio          dados
```

- **Modelos** (`src/models`): as entidades do domínio (Aluno, Turma, Matrícula, ...).
- **Repositórios** (`src/repositories`): acesso à base de dados (SQL), um por entidade principal.
- **Serviços** (`src/services`): as regras de negócio e validações; orquestram os repositórios.
- **Interface** (`main.py`): menu de consola que liga os perfis de utilizador às funcionalidades.

## Estrutura de pastas

```
Projeto LinguaViva/
├── db/
│   ├── connection.py      # ligação à BD e inicialização (get_connection / inicializar_bd)
│   └── schema.sql         # definição das tabelas
├── src/
│   ├── models/            # entidades do domínio
│   ├── repositories/      # acesso a dados
│   └── services/          # regras de negócio
├── tests/
│   └── test_aluno_service.py
├── main.py                # ponto de entrada (menu)
├── .gitignore
└── README.md
```

## Requisitos

- **Python 3.10** ou superior
- **SQLite** (incluído no módulo `sqlite3` da biblioteca-padrão do Python — nada a instalar)

## Como executar

A partir da raiz do projeto:

```bash
python main.py
```

No primeiro arranque, a base de dados (`db/linguaviva.db`) é **criada automaticamente** a partir
do `db/schema.sql` — não é preciso configurar nada. O ficheiro `.db` não é versionado no
repositório; é sempre gerado localmente.

### Menus disponíveis

```
Menu Principal
 1. Secretaria             (gestão completa: alunos, professores, turmas, matrículas, certificados)
 2. Professor              (registar aulas, presenças e avaliações)
 3. Direção                (relatórios de assiduidade e de aprovados)
 4. Encarregado de Educação (consultar histórico do educando)
 0. Sair
```

## Testes

Testes unitários da camada de serviço (com `unittest` e `MagicMock`):

```bash
python -m unittest tests.test_aluno_service -v
```

## Base de dados

Modelo relacional em SQLite com as entidades: `Aluno`, `EncarregadoEducacao`, `Professor`,
`Idioma`, `Nivel`, `Turma`, `Matricula`, `Aula`, `Presenca`, `Avaliacao`, `Certificado` e
`Utilizador`. O esquema completo está em [`db/schema.sql`](db/schema.sql).

Para inspecionar a base de dados no terminal:

```bash
sqlite3 db/linguaviva.db
```
