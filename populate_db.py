import sqlite3
import random
from datetime import datetime

# Conectar ao banco de dados
conn = sqlite3.connect('instance/medical_clinic.sqlite')
cur = conn.cursor()

# Excluir tabelas se já existirem
cur.execute('DROP TABLE IF EXISTS fluxo_atendimento')
cur.execute('DROP TABLE IF EXISTS paciente')
cur.execute('DROP TABLE IF EXISTS diagnostico')
cur.execute('DROP TABLE IF EXISTS servico_manejo')
cur.execute('DROP TABLE IF EXISTS servico_especializado')

# Criar tabelas
cur.execute('''
    CREATE TABLE IF NOT EXISTS servico_especializado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS servico_manejo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS diagnostico (
        cid TEXT PRIMARY KEY,
        descricao TEXT NOT NULL,
        servico_especializado_id INTEGER,
        servico_manejo_ids TEXT,
        incluir_no_algoritmo INTEGER DEFAULT 0,
        FOREIGN KEY (servico_especializado_id) REFERENCES servico_especializado (id)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS paciente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        diagnostico TEXT NOT NULL,
        cid TEXT NOT NULL,
        FOREIGN KEY (cid) REFERENCES diagnostico (cid)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS fluxo_atendimento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        diagnostico_cid TEXT,
        etapa TEXT,
        data TEXT,
        proximo_passo TEXT,
        FOREIGN KEY (paciente_id) REFERENCES paciente (id),
        FOREIGN KEY (diagnostico_cid) REFERENCES diagnostico (cid)
    )
''')

# Adicionar serviços especializados
cur.executemany('''
    INSERT OR IGNORE INTO servico_especializado (nome)
    VALUES (?)
''', [('Neurologia',), ('Cardiologia',), ('Endocrinologia',)])

# Adicionar serviços de manejo
cur.executemany('''
    INSERT OR IGNORE INTO servico_manejo (nome)
    VALUES (?)
''', [('Fisioterapia',), ('Psicologia',)])

# Adicionar diagnósticos
diagnosticos = [
    ('I69.4', 'Sequela de acidente vascular cerebral', 1, '1,2'),
    ('I10', 'Hipertensão arterial', 2, ''),
    ('E11', 'Diabetes mellitus tipo 2', 3, ''),
    ('J45', 'Asma', 2, ''),
    ('F32', 'Episódio depressivo', 2, '2'),
    ('M54.5', 'Dor lombar', 1, '1'),
    ('G40', 'Epilepsia', 1, '1,2'),
    ('K21', 'Doença do refluxo gastroesofágico', 2, ''),
    ('L20', 'Dermatite atópica', 3, ''),
    ('N39.0', 'Infecção do trato urinário', 2, ''),
    ('H52', 'Transtornos da refração e da acomodação', 1, ''),
]

cur.executemany('''
    INSERT OR IGNORE INTO diagnostico (cid, descricao, servico_especializado_id, servico_manejo_ids)
    VALUES (?, ?, ?, ?)
''', diagnosticos)

# Adicionar pacientes e fluxos de atendimento
nomes = [f'Paciente {i}' for i in range(1, 301)]
diagnosticos = [
    'Sequela de acidente vascular cerebral', 'Hipertensão arterial', 'Diabetes mellitus tipo 2',
    'Asma', 'Episódio depressivo', 'Dor lombar', 'Epilepsia', 'Doença do refluxo gastroesofágico',
    'Dermatite atópica', 'Infecção do trato urinário', 'Transtornos da refração e da acomodação'
]
cids = ['I69.4', 'I10', 'E11', 'J45', 'F32', 'M54.5', 'G40', 'K21', 'L20', 'N39.0', 'H52']
etapas = ['Diagnóstico', 'Manejo', 'Acompanhamento']
proximos_passos = ['Manejo', 'Acompanhamento']

pacientes = []
fluxos = []

for i, nome in enumerate(nomes):
    diagnostico = random.choice(diagnosticos)
    cid = cids[diagnosticos.index(diagnostico)]
    etapa = random.choice(etapas)
    proximo_passo = random.choice(proximos_passos)
    pacientes.append((nome, diagnostico, cid))
    fluxos.append((i + 1, cid, etapa, datetime.now().strftime('%Y-%m-%d'), proximo_passo))

cur.executemany('''
    INSERT INTO paciente (nome, diagnostico, cid)
    VALUES (?, ?, ?)
''', pacientes)

cur.executemany('''
    INSERT INTO fluxo_atendimento (paciente_id, diagnostico_cid, etapa, data, proximo_passo)
    VALUES (?, ?, ?, ?, ?)
''', fluxos)

# Confirmar adições ao banco de dados
conn.commit()

# Fechar conexão
conn.close()

print("Banco de dados populado com sucesso!")
