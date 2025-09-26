"""
gerar_julgados_254k.py
Gera CSV com 254.458 processos fictícios e realistas, com muitas variáveis e erros de coleta.
"""

import csv
import os
import random
from faker import Faker
from datetime import datetime, timedelta

# ----------------- CONFIGURAÇÃO -----------------
NUM_REGISTROS = 54458
SAIDA_DIR = "julgados_csv"
NOME_ARQUIVO = os.path.join(SAIDA_DIR, "julgados_1.csv")

# Tribunal que apresentará taxa de erro maior (ex.: 'TJSP')
TRIBUNAL_COM_MAIS_ERROS = "TJSP"
TAXA_ERRO_PADRAO = 0.10      # 10% chance de erro por registro (baseline)
TAXA_ERRO_TRIBUNAL_ALTO = 0.30  # 30% quando o processo pertence ao tribunal 'problemático'

SEED = 42  # para reprodutibilidade (opcional)
# -------------------------------------------------

random.seed(SEED)
fake = Faker("pt_BR")
os.makedirs(SAIDA_DIR, exist_ok=True)

# ----------------- LISTAS BASE (mais realistas) -----------------
# Tribunais (estaduais, TRF, TRE, TRT, superiores)
tribunais = [
    # Exemplos de TJs (siglas)
    "TJAC","TJAL","TJAP","TJAM","TJBA","TJCE","TJDFT","TJES","TJGO","TJMA","TJMT","TJMS",
    "TJPB","TJPB","TJPE","TJPI","TJPR","TJRJ","TJRN","TJRS","TJRO","TJRR","TJSC","TJSP","TJSE","TJTO",
    # TRFs
    "TRF1","TRF2","TRF3","TRF4","TRF5",
    # Tribunais Superiores
    "STF","STJ","STM",
    # TREs (siglas)
    "TRE-AC","TRE-AL","TRE-AP","TRE-AM","TRE-BA","TRE-CE","TRE-DF","TRE-ES","TRE-GO","TRE-MA","TRE-MT","TRE-MS",
    "TRE-MG","TRE-PA","TRE-PB","TRE-PR","TRE-PE","TRE-PI","TRE-RJ","TRE-RN","TRE-RS","TRE-RO","TRE-RR","TRE-SC","TRE-SP","TRE-SE","TRE-TO",
    # TRTs (alguns exemplos)
    "TRT1","TRT2","TRT3","TRT4","TRT5","TRT6","TRT7","TRT8","TRT9","TRT10","TRT11","TRT12","TRT13","TRT14","TRT15","TRT16",
    "TRT17","TRT18","TRT19","TRT20","TRT21","TRT22","TRT23","TRT24","TRT25"
]

# Varas de origem simuladas (100 varas)
varas_origem = [f"Vara Cível {i}" for i in range(1, 101)]

# Recursos possíveis (nomes)
recursos = ["Apelação", "Recurso Especial", "Agravo", "Embargos de Declaração", "Mandado de Segurança", "Apelação Cível", "Recurso Ordinário"]

# Outros campos
relatores = [f"Des./Min. {fake.last_name()}" for _ in range(200)]
assuntos = [
    "Direito do Consumidor", "Direito Trabalhista", "Direito Penal", "Direito Civil",
    "Direito Tributário", "Direito Administrativo", "Direito Constitucional",
    "Direito Empresarial", "Direito Ambiental", "Direito Previdenciário"
]
decisoes = [
    "Recurso provido", "Recurso não provido", "Sentença mantida",
    "Sentença reformada", "Pedido indeferido", "Pedido deferido"
]
tipos_acao = ["Ação Ordinária", "Mandado de Segurança", "Recurso Especial", "Apelação", "Agravo"]
instancias = ["1ª Instância", "2ª Instância", "3ª Instância", "Turma", "Plenário"]
fundamentos = [
    "com base no princípio da legalidade",
    "à luz do devido processo legal",
    "segundo entendimento pacífico do STJ",
    "em respeito ao contraditório e ampla defesa",
    "de acordo com súmula vinculante aplicável",
    "considerando a ausência de provas robustas",
    "diante da comprovação da relação de consumo",
    "em virtude da prescrição reconhecida",
    "pela aplicação da teoria do risco integral",
    "observando a responsabilidade objetiva da Administração"
]
consequencias = [
    "determinando a restituição em dobro dos valores pagos",
    "mantendo a condenação em danos morais",
    "afastando a responsabilidade da parte requerida",
    "anulando o ato administrativo impugnado",
    "determinando a reintegração do empregado",
    "fixando nova dosimetria da pena",
    "ordenando a reabertura da instrução processual",
    "estabelecendo a obrigação de fazer",
    "reconhecendo a nulidade contratual",
    "determinando a suspensão da exigibilidade do crédito tributário"
]
equipes_coleta = [f"Equipe {c}" for c in ("A","B","C","D","E","F","G")]

# Cabeçalho final (muitas variáveis)
colunas = [
    "processo", "tribunal", "vara_origem", "tribunal_origem", "relator", "assunto", "decisao", "ementa",
    "data_distribuicao", "data_julgamento", "tipo_acao", "parte_autora", "parte_re", "advogado_autor", "advogado_re",
    "instancia", "valor_acao", "valor_custas", "numero_paginas", "numero_testemunhas", "numero_peritos",
    "numero_documento", "numero_protocolo", "numero_recurso", "recurso_interposto", "sentenca_anterior",
    "recurso_pendente", "parecer_mp", "relatorio_tecnico", "observacoes", "fundamentacao", "conclusao",
    "audiencia_realizada", "tempo_tramitacao_dias", "prescricao_geral", "decisao_publicada",
    "data_recurso", "juiz_suplente", "responsavel_digitacao", "versao_sistema", "referencia_legislativa",
    "tipo_documento", "orgao_emissor", "local_julgamento", "publico_alvo", "data_coleta", "lote_coleta", "equipe_coleta",
    "erro_coleta", "erro_tipo"  # erro_tipo descreve qual tipo de erro foi injetado
]

# ----------------- FUNÇÕES AUXILIARES -----------------
def gerar_numero_processo(existing_set):
    # Formato simples mas único: 7 dígitos + '-' + 2 dígitos + '.' + ano + '.' + tribunalCodigo + '.' + 4 dígitos
    while True:
        num = f"{random.randint(10**6, 10**7-1)}-{random.randint(10,99)}.{random.randint(2015,2025)}.{random.randint(1,99)}.{random.randint(1000,9999)}"
        if num not in existing_set:
            existing_set.add(num)
            return num

def gerar_ementa_long(assunto, decisao):
    # Gera 2-5 frases combinando fundamentos e consequencias para parecer realista
    partes = []
    partes.append(f"Ementa: {assunto}. {decisao}.")
    n_paragrafos = random.randint(1,3)
    for _ in range(n_paragrafos):
        partes.append(fake.paragraph(nb_sentences=random.randint(2,6)))
    partes.append(f"{random.choice(fundamentos).capitalize()}, {random.choice(consequencias)}.")
    return " ".join(partes)

def escolher_taxa_erro(tribunal):
    return TAXA_ERRO_TRIBUNAL_ALTO if tribunal == TRIBUNAL_COM_MAIS_ERROS else TAXA_ERRO_PADRAO

def inject_errors(record_dict, taxa_erro):
    """
    Dado um dicionário com campos, injeta erros conforme taxa_erro.
    Retorna (erro_bool, erro_tipo_string).
    Tipos de erro possíveis: 'vazio', 'nulo', 'invalido', 'data_malformada', 'ementa_erro', 'num_negativo', 'tribunal_errado'
    """
    erro_tipo = []
    erro_flag = False

    # Para cada campo, com certa probabilidade, introduz um erro específico
    # Ex.: deixar tribunal vazio
    if random.random() < taxa_erro * 0.25:
        record_dict["tribunal"] = ""  # campo vazio
        erro_flag = True
        erro_tipo.append("tribunal_vazio")

    # relator vira None
    if random.random() < taxa_erro * 0.12:
        record_dict["relator"] = None
        erro_flag = True
        erro_tipo.append("relator_nulo")

    # assunto inválido
    if random.random() < taxa_erro * 0.10:
        record_dict["assunto"] = "INDEFINIDO"
        erro_flag = True
        erro_tipo.append("assunto_invalido")

    # decisao vazia
    if random.random() < taxa_erro * 0.10:
        record_dict["decisao"] = ""
        erro_flag = True
        erro_tipo.append("decisao_vazia")

    # ementa com texto de erro
    if random.random() < taxa_erro * 0.15:
        record_dict["ementa"] = "ERRO DE COLETA: texto ausente"
        erro_flag = True
        erro_tipo.append("ementa_erro")

    # data_distribution ou data_julgamento malformada
    if random.random() < taxa_erro * 0.12:
        record_dict["data_distribuicao"] = "32/13/9999"  # data inválida
        erro_flag = True
        erro_tipo.append("data_malformada")

    if random.random() < taxa_erro * 0.08:
        record_dict["valor_acao"] = -abs(record_dict.get("valor_acao", 0))  # valor negativo
        erro_flag = True
        erro_tipo.append("valor_negativo")

    # numero_documento com formato errado
    if random.random() < taxa_erro * 0.06:
        record_dict["numero_documento"] = "SEM_NUMERO"
        erro_flag = True
        erro_tipo.append("doc_invalido")

    # data_coleta vazia ou antecedente (simula erro)
    if random.random() < taxa_erro * 0.07:
        record_dict["data_coleta"] = ""  # vazio
        erro_flag = True
        erro_tipo.append("data_coleta_vazia")

    # ocasionalmente tribunal incorreto (ex.: sigla inexistente)
    if random.random() < taxa_erro * 0.04:
        record_dict["tribunal"] = "XXX"
        erro_flag = True
        erro_tipo.append("tribunal_invalido")

    # se nenhum erro foi marcado, mantenha erro_flag False
    return erro_flag, ";".join(erro_tipo) if erro_tipo else ""

# ----------------- GERAÇÃO DO CSV -----------------
existing_processos = set()

with open(NOME_ARQUIVO, mode="w", newline="", encoding="utf-8") as fh:
    writer = csv.writer(fh)
    writer.writerow(colunas)

    for i in range(NUM_REGISTROS):
        # Escolhe tribunal (aleatório)
        tribunal = random.choice(tribunais)
        taxa_erro_atual = escolher_taxa_erro(tribunal)

        processo = gerar_numero_processo(existing_processos)
        vara_origem = random.choice(varas_origem)
        tribunal_origem = random.choice(tribunais)
        relator = random.choice(relatores)
        assunto = random.choice(assuntos)
        decisao = random.choice(decisoes)
        ementa = gerar_ementa_long(assunto, decisao)
        data_distribuicao = fake.date_between(start_date='-6y', end_date='today').strftime("%Y-%m-%d")
        data_julgamento = fake.date_between(start_date='-5y', end_date='today').strftime("%Y-%m-%d")
        tipo_acao = random.choice(tipos_acao)
        parte_autora = fake.name()
        parte_re = fake.name()
        advogado_autor = fake.name()
        advogado_re = fake.name()
        instancia = random.choice(instancias)
        valor_acao = round(random.uniform(500.0, 1_000_000.0), 2)
        valor_custas = round(random.uniform(50.0, 10000.0), 2)
        numero_paginas = random.randint(1, 500)
        numero_testemunhas = random.randint(0, 10)
        numero_peritos = random.randint(0, 5)
        numero_documento = f"{random.randint(10**6,10**9-1)}"
        numero_protocolo = f"P-{random.randint(100000,999999)}"
        numero_recurso = f"R-{random.randint(1000000,9999999)}"
        recurso_interposto = random.choice(recursos)
        sentenca_anterior = random.choice(["Sim", "Não"])
        recurso_pendente = random.choice(["Sim", "Não"])
        parecer_mp = random.choice(["Favorável", "Desfavorável", "Ausente"])
        relatorio_tecnico = fake.sentence(nb_words=10)
        observacoes = fake.sentence(nb_words=12)
        fundamentacao = gerar_ementa_long(assunto, decisao)[:300]  # trecho curto
        conclusao = fake.sentence(nb_words=15)
        audiencia_realizada = random.choice(["Sim", "Não"])
        tempo_tramitacao_dias = random.randint(0, 3650)
        prescricao_geral = random.choice(["Sim", "Não"])
        decisao_publicada = random.choice(["Sim", "Não"])
        data_recurso = fake.date_between(start_date='-4y', end_date='today').strftime("%Y-%m-%d")
        juiz_suplente = fake.name()
        responsavel_digitacao = fake.name()
        versao_sistema = f"v{random.randint(1,5)}.{random.randint(0,9)}"
        referencia_legislativa = f"Art. {random.randint(1,500)}"
        tipo_documento = random.choice(["Despacho", "Sentença", "Acórdão", "Decisão interlocutória"])
        orgao_emissor = fake.company()
        local_julgamento = fake.city()
        publico_alvo = random.choice(["Público", "Privado"])
        data_coleta = fake.date_between(start_date='-1y', end_date='today').strftime("%Y-%m-%d")
        lote_coleta = f"Lote {random.randint(1,500)}"
        equipe_coleta = random.choice(equipes_coleta)

        # Monta dicionário do registro
        record = {
            "processo": processo,
            "tribunal": tribunal,
            "vara_origem": vara_origem,
            "tribunal_origem": tribunal_origem,
            "relator": relator,
            "assunto": assunto,
            "decisao": decisao,
            "ementa": ementa,
            "data_distribuicao": data_distribuicao,
            "data_julgamento": data_julgamento,
            "tipo_acao": tipo_acao,
            "parte_autora": parte_autora,
            "parte_re": parte_re,
            "advogado_autor": advogado_autor,
            "advogado_re": advogado_re,
            "instancia": instancia,
            "valor_acao": valor_acao,
            "valor_custas": valor_custas,
            "numero_paginas": numero_paginas,
            "numero_testemunhas": numero_testemunhas,
            "numero_peritos": numero_peritos,
            "numero_documento": numero_documento,
            "numero_protocolo": numero_protocolo,
            "numero_recurso": numero_recurso,
            "recurso_interposto": recurso_interposto,
            "sentenca_anterior": sentenca_anterior,
            "recurso_pendente": recurso_pendente,
            "parecer_mp": parecer_mp,
            "relatorio_tecnico": relatorio_tecnico,
            "observacoes": observacoes,
            "fundamentacao": fundamentacao,
            "conclusao": conclusao,
            "audiencia_realizada": audiencia_realizada,
            "tempo_tramitacao_dias": tempo_tramitacao_dias,
            "prescricao_geral": prescricao_geral,
            "decisao_publicada": decisao_publicada,
            "data_recurso": data_recurso,
            "juiz_suplente": juiz_suplente,
            "responsavel_digitacao": responsavel_digitacao,
            "versao_sistema": versao_sistema,
            "referencia_legislativa": referencia_legislativa,
            "tipo_documento": tipo_documento,
            "orgao_emissor": orgao_emissor,
            "local_julgamento": local_julgamento,
            "publico_alvo": publico_alvo,
            "data_coleta": data_coleta,
            "lote_coleta": lote_coleta,
            "equipe_coleta": equipe_coleta,
        }

        # Injeta erros conforme taxa do tribunal
        erro_flag, erro_tipo = inject_errors(record, taxa_erro_atual)
        record["erro_coleta"] = erro_flag
        record["erro_tipo"] = erro_tipo

        # Escreve linha no CSV seguindo a ordem das colunas
        writer.writerow([record.get(c) for c in colunas])

        # (Opcional) progresso simples a cada 10k registros
        if (i+1) % 10000 == 0:
            print(f"{i+1} registros gerados...")

print(f"\nCSV com {NUM_REGISTROS} processos gerados em: {NOME_ARQUIVO}")
