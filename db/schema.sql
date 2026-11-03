PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS EncarregadoEducacao (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    nif         TEXT,
    telefone    TEXT,
    email       TEXT,
    parentesco  TEXT
);

CREATE TABLE IF NOT EXISTS Professor (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    telefone    TEXT,
    email       TEXT,
    custo_hora  REAL,
    ativo       INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS Idioma (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome    TEXT NOT NULL,
    codigo  TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Nivel (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo               TEXT NOT NULL UNIQUE,
    descricao            TEXT,
    ponderacao_oral      REAL NOT NULL,
    ponderacao_escrito   REAL NOT NULL,
    ponderacao_projeto   REAL NOT NULL,
    CHECK (ponderacao_oral + ponderacao_escrito + ponderacao_projeto = 1)
);

CREATE TABLE IF NOT EXISTS Aluno (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT    NOT NULL,
    nif                 TEXT    UNIQUE,
    data_nasc           TEXT,
    telefone            TEXT,
    email               TEXT,
    morada              TEXT,
    enc_educacao_id     INTEGER,
    consentimento_rgpd  INTEGER NOT NULL DEFAULT 0 CHECK (consentimento_rgpd IN (0, 1)),
    data_consentimento  TEXT,
    ativo               INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    FOREIGN KEY (enc_educacao_id) REFERENCES EncarregadoEducacao (id)
);

CREATE TABLE IF NOT EXISTS ProfessorIdioma (
    professor_id  INTEGER NOT NULL,
    idioma_id     INTEGER NOT NULL,
    PRIMARY KEY (professor_id, idioma_id),
    FOREIGN KEY (professor_id) REFERENCES Professor (id),
    FOREIGN KEY (idioma_id)    REFERENCES Idioma (id)
);

CREATE TABLE IF NOT EXISTS Turma (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    idioma_id     INTEGER NOT NULL,
    nivel_id      INTEGER NOT NULL,
    professor_id  INTEGER NOT NULL,
    horario       TEXT,
    sala          TEXT,
    max_alunos    INTEGER NOT NULL DEFAULT 12 CHECK (max_alunos BETWEEN 6 AND 12),
    semestre      INTEGER,
    ano           INTEGER,
    ativa         INTEGER NOT NULL DEFAULT 1 CHECK (ativa IN (0, 1)),
    FOREIGN KEY (idioma_id)    REFERENCES Idioma (id),
    FOREIGN KEY (nivel_id)     REFERENCES Nivel (id),
    FOREIGN KEY (professor_id) REFERENCES Professor (id)
);

CREATE TABLE IF NOT EXISTS Matricula (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id       INTEGER NOT NULL,
    turma_id       INTEGER NOT NULL,
    data_matricula TEXT    NOT NULL,
    valor_propina  REAL,
    estado         TEXT    NOT NULL DEFAULT 'ativa'
                   CHECK (estado IN ('ativa', 'cancelada', 'concluida')),
    nota_final     REAL,
    UNIQUE (aluno_id, turma_id),
    FOREIGN KEY (aluno_id) REFERENCES Aluno (id),
    FOREIGN KEY (turma_id) REFERENCES Turma (id)
);

CREATE TABLE IF NOT EXISTS Aula (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    turma_id      INTEGER NOT NULL,
    professor_id  INTEGER NOT NULL,
    data          TEXT    NOT NULL,
    sumario       TEXT,
    FOREIGN KEY (turma_id)     REFERENCES Turma (id),
    FOREIGN KEY (professor_id) REFERENCES Professor (id)
);

CREATE TABLE IF NOT EXISTS Presenca (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    aula_id       INTEGER NOT NULL,
    matricula_id  INTEGER NOT NULL,
    estado        TEXT    NOT NULL CHECK (estado IN ('P', 'A', 'J')),
    UNIQUE (aula_id, matricula_id),
    FOREIGN KEY (aula_id)      REFERENCES Aula (id),
    FOREIGN KEY (matricula_id) REFERENCES Matricula (id)
);

CREATE TABLE IF NOT EXISTS Avaliacao (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula_id  INTEGER NOT NULL,
    tipo          TEXT    NOT NULL CHECK (tipo IN ('oral', 'escrito', 'projeto')),
    nota          REAL    NOT NULL CHECK (nota BETWEEN 0 AND 20),
    data          TEXT    NOT NULL,
    FOREIGN KEY (matricula_id) REFERENCES Matricula (id)
);

CREATE TABLE IF NOT EXISTS Certificado (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula_id       INTEGER NOT NULL UNIQUE,
    numero_certificado TEXT    NOT NULL UNIQUE,
    data_emissao       TEXT    NOT NULL,
    ficheiro_pdf       TEXT,
    FOREIGN KEY (matricula_id) REFERENCES Matricula (id)
);

CREATE TABLE IF NOT EXISTS Utilizador (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    username       TEXT    NOT NULL UNIQUE,
    password_hash  TEXT    NOT NULL,
    perfil         TEXT    NOT NULL
                   CHECK (perfil IN ('Secretaria', 'Professor', 'Direcao')),
    professor_id   INTEGER,
    ativo          INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    FOREIGN KEY (professor_id) REFERENCES Professor (id)
);
