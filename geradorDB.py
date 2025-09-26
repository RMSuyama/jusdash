import csv
import os
import random

# Configurações
NUM_ARQUIVOS = 1
REGISTROS_POR_ARQUIVO = 50000
PASTA_SAIDA = "julgados_csv"

os.makedirs(PASTA_SAIDA, exist_ok=True)

# Listas base (serão combinadas para gerar mais de 1000 variações)
tribunais = ["TJSP", "TJMG", "TJRS", "TRF1", "TRF3", "STJ", "STF"]

relatores = [
    "Min. Silva", "Min. Souza", "Des. Oliveira", "Des. Lima", "Juiz Pereira",
    "Min. Barros", "Des. Andrade", "Juiz Costa", "Min. Rocha", "Des. Fernandes"
]

assuntos = [
    "Direito do Consumidor", "Direito Trabalhista", "Direito Penal", "Direito Civil",
    "Direito Tributário", "Direito Administrativo", "Direito Constitucional",
    "Direito Empresarial", "Direito Ambiental", "Direito Previdenciário"
]

decisoes = [
    "Recurso provido", "Recurso não provido", "Sentença mantida",
    "Sentença reformada", "Pedido indeferido", "Pedido deferido"
]

# Listas expandidas para gerar variedade
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

# Gera um processo fictício
def gerar_numero_processo():
    return f"{random.randint(1000000, 9999999)}-{random.randint(10, 99)}.{random.randint(2020, 2025)}.{random.randint(1, 99)}.{random.randint(1000, 9999)}"

# Gera ementa com combinações aleatórias
def gerar_ementa(assunto, decisao):
    return (
        f"Ementa: {assunto}. {decisao}, {random.choice(fundamentos)}, "
        f"{random.choice(consequencias)}."
    )

# Criação dos CSVs
for i in range(1, NUM_ARQUIVOS + 1):
    nome_arquivo = os.path.join(PASTA_SAIDA, f"julgados_{i}.csv")
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["processo", "tribunal", "relator", "assunto", "decisao", "ementa"])
        
        for _ in range(REGISTROS_POR_ARQUIVO):
            assunto = random.choice(assuntos)
            decisao = random.choice(decisoes)
            writer.writerow([
                gerar_numero_processo(),
                random.choice(tribunais),
                random.choice(relatores),
                assunto,
                decisao,
                gerar_ementa(assunto, decisao)
            ])

print(f"{NUM_ARQUIVOS} arquivos CSV com ementas gerados em: {PASTA_SAIDA}")
