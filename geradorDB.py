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
NUM_REGISTROS = 35443
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
varas_origem = [f"Vara Cível {i}" for i in range(1, 5)]

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
    "observando a responsabilidade objetiva da Administração",
    "à luz do princípio da dignidade da pessoa humana",
    "com base no artigo 5º da Constituição Federal",
    "segundo orientação consolidada do STF",
    "em consonância com a jurisprudência dominante",
    "considerando a vedação ao enriquecimento sem causa",
    "diante da comprovação da má-fé processual",
    "pela aplicação do princípio da razoabilidade",
    "com fundamento no princípio da proporcionalidade",
    "em respeito ao princípio da segurança jurídica",
    "de acordo com o Código de Defesa do Consumidor",
    "à luz da teoria da perda de uma chance",
    "com base na interpretação teleológica da norma",
    "considerando a coisa julgada material",
    "em virtude da incompetência absoluta reconhecida",
    "diante da inexistência de pressupostos processuais",
    "pela aplicação da teoria da imprevisão",
    "em consonância com o princípio da eficiência administrativa",
    "segundo a vedação ao bis in idem",
    "observando a teoria do adimplemento substancial",
    "com base no princípio da moralidade administrativa",
    "em respeito à separação de poderes",
    "pela aplicação do princípio da continuidade do serviço público",
    "considerando a ausência de interesse de agir",
    "diante da inépcia da inicial reconhecida",
    "à luz da supremacia do interesse público",
    "com fundamento na autotutela administrativa",
    "em virtude da presunção de legitimidade do ato administrativo",
    "segundo a teoria do fato consumado",
    "considerando a aplicação do princípio da precaução",
    "pela observância da função social do contrato",
    "diante da vedação à analogia in malam partem",
    "em respeito ao princípio da anterioridade tributária",
    "à luz da proteção da confiança legítima",
    "com fundamento no artigo 37 da Constituição Federal",
    "em virtude da teoria do domínio do fato",
    "considerando a responsabilidade civil subjetiva",
    "diante da ausência de nexo causal",
    "pela aplicação da teoria do patrimônio mínimo",
    "em respeito à vedação do retrocesso social"
]

consequencias = [
"anulando a extinção do processo sem resolução do mérito com publicação oficial",
"reiterando a restituição em dobro dos valores pagos",
"substituindo a nulidade do ato administrativo",
"estabelecendo o reconhecimento da ocorrência de fraude com remessa dos autos à instância superior",
"revogando a obrigação de fazer com suspensão de efeitos administrativos",
"reparando a extinção do processo sem resolução do mérito com repetição do indébito",
"reparando a condenação em danos morais com multa diária por descumprimento",
"confirmando a concessão de liminar",
"deferindo a correção monetária do débito com efeitos retroativos",
"ratificando a condenação em danos morais com determinação de remessa ao Ministério Público",
"determinando a restituição em dobro dos valores pagos pelo fundamento do enriquecimento ilícito",
"mantendo a condenação em danos morais em razão da violação contratual",
"afastando a responsabilidade da parte requerida por ausência de prova robusta",
"anulando o ato administrativo impugnado diante da má-fé comprovada",
"determinando a reintegração do empregado em conformidade com a súmula aplicável",
"fixando nova dosimetria da pena por ilegalidade do ato",
"ordenando a reabertura da instrução processual subsidiariamente, com reversão dos valores",
"estabelecendo a obrigação de fazer com aplicação de juros e correção monetária",
"reconhecendo a nulidade contratual sem prejuízo de eventual reparação suplementar",
"determinando a suspensão da exigibilidade do crédito tributário nos termos da jurisprudência dominante",
"determinando a restituição imediata com imposição de medidas cautelares",
"condenando ao ressarcimento integral dos valores com efeito ex nunc",
"absolvendo com efeitos retroativos",
"reconhecendo a ocorrência de enriquecimento ilícito com repetição do indébito",
"estabelecendo a obrigação de indenizar com restituição imediata",
"fixando a indenização por danos materiais com inabilitação temporária da parte",
"ordenando o ressarcimento com perda do direito de recurso",
"suspendendo a exigibilidade com publicação oficial",
"indeferindo o pedido condicionado à apresentação de documentos",
"deferindo a pretensão com sujeição à homologação judicial",
"revogando o ato administrativo com suspensão de efeitos administrativos",
"confirmando a sentença com designação de audiência de conciliação",
"modificando a decisão com expedição de mandado de busca e apreensão",
"restituindo os valores pagos com aplicação de juros e correção monetária",
"reconhecendo a responsabilidade solidária com imposição de multa diária por descumprimento",
"anulando cláusula contratual por afronta aos princípios constitucionais",
"determinando a reparação integral dos prejuízos com intimação da autoridade competente",
"mantendo a condenação com remessa dos autos à instância superior",
"afastando a responsabilidade em razão de prescrição com observância do contraditório",
"anulando o ato por nulidade formal com remessa ao Ministério Público",
"determinando a devolução dos bens apreendidos com imposição de medidas cautelares",
"condenando em honorários advocatícios nos termos da jurisprudência dominante",
"ordenando a correção do registro com restituição em dobro dos valores pagos",
"reconhecendo a nulidade do título executivo com compensação dos valores pagos em excesso",
"determinando a reintegração imediata com restituição de salários",
"fixando nova dosimetria da pena com aplicação de atenuantes",
"ordenando a reabertura da instrução processual para produção de prova pericial",
"estabelecendo a obrigação de fazer com prazo máximo de cumprimento",
"reconhecendo a nulidade contratual e declarando a rescisão",
"determinando a suspensão da exigibilidade do crédito tributário com condicionamento à apresentação de garantias",
"determinando a restituição em dobro e a indenização por danos morais",
"mantendo a condenação em danos morais sem redução do quantum",
"afastando a responsabilidade por falta de nexo causal",
"anulando o ato por vício de competência",
"determinando a reintegração do empregado com pagamento de verbas rescisórias",
"fixando nova dosimetria e reduzindo a pena-base",
"ordenando a reabertura por cerceamento de defesa",
"estabelecendo obrigação de fazer e fixando multa diária",
"reconhecendo a nulidade contratual com restituição proporcional",
"determinando a suspensão do crédito tributário até decisão final",
"condenando ao pagamento de custas processuais e honorários",
"mantendo a sentença por ausência de recursos admissíveis",
"anulando a decisão por vício de motivação",
"determinando a restituição integral em face da relação de consumo",
"reconhecendo a responsabilização objetiva com obrigação de indenizar",
"determinando a suspensão do processo por dependência de sentença",
"mantendo a condenação por prova robusta",
"afastando a responsabilidade diante de caso fortuito",
"anulando atos por violação do devido processo legal",
"determinando a reintegração com ressarcimento de danos emergentes",
"fixando pena acessória e aplicação de multa",
"ordenando nova instrução com produção de prova testemunhal",
"estabelecendo obrigação de fazer e reparação por perdas e danos",
"reconhecendo a nulidade contratual por cláusula abusiva",
"determinando a suspensão da exigibilidade tributária por ausência de lançamento regular",
"condenando ao ressarcimento com retenção judicial de valores",
"mantendo a condenação com aplicação de súmula",
"afastando a responsabilidade por falta de culpa",
"anulando despacho por incompetência",
"determinando a restituição em dobro com juros de mora",
"reconhecendo responsabilidade solidária e partilha do débito",
"determinando a reintegração e a reintegração de funções",
"fixando nova dosimetria com agravantes reconhecidos",
"ordenando a reabertura para complemento probatório",
"estabelecendo obrigação de fazer e multa cominatória",
"reconhecendo nulidade por vício de consentimento",
"determinando suspensão de efeitos administrativos cautelarmente",
"condenando em honorários proporcionais ao trabalho",
"mantendo a sentença por insuficiência recursal",
"afastando responsabilidade pelo caso fortuito externo",
"anulando ato por cerceamento de defesa",
"determinando a restituição com atualização monetária",
"reconhecendo responsabilidade e fixando indenização por dano moral",
"determinando a suspensão do crédito com a apresentação de garantias",
"condenando ao pagamento de custas e cominação de multa",
"mantendo entendimento anterior com base em precedente",
"afastando responsabilidade por manifesta ausência de ilicitude",
"anulando a decisão por nulidade insanável",
"determinando a restituição em dobro com aplicação de multa",
"reconhecendo a nulidade contratual e declarando a rescisão unilateral",
"determinando a reintegração do empregado com ressarcimento total",
"fixando nova dosimetria e substituindo pena privativa por multa",
"ordenando a reabertura com requisição de documentos",
"estabelecendo obrigação de fazer e fixando prazo peremptório",
"reconhecendo a nulidade por fraude na celebração do contrato",
"determinando a suspensão da exigibilidade do crédito tributário com efeitos imediatos",
"condenando a parte ao pagamento de indenização por lucros cessantes",
"mantendo a condenação com majoração do quantum indenizatório",
"afastando a responsabilidade por ausência de nexo técnico",
"anulando ato por vício formal insanável",
"determinando restituição e compensação de valores pagos indevidamente",
"reconhecendo a nulidade do ato administrativo e determinando sua revogação",
"determinando reintegração com estabilidade provisória",
"fixando nova dosimetria fundamentada em precedente vinculante",
"ordenando a reabertura por prova nova nos autos",
"estabelecendo obrigação de fazer com tutela específica",
"reconhecendo a nulidade contratual por vício redibitório",
"determinando a suspensão da exigibilidade até o trânsito em julgado",
"condenando ao pagamento de multa administrativa e reparação civil",
"mantendo a sentença por interpretação literal da norma",
"afastando a responsabilidade pela ausência de conduta dolosa",
"anulando despacho por incompetência territorial",
"determinando a restituição em dobro e a compensação de danos",
"reconhecendo a responsabilidade objetiva e fixando obrigação de indenizar",
"determinando reintegração e pagamento de salários retroativos",
"fixando nova dosimetria e aplicando regime inicial impeditivo",
"ordenando reabertura por nulidade de citação",
"estabelecendo obrigação de fazer e fornecimento imediato do serviço",
"reconhecendo a nulidade contratual por abusividade de cláusula",
"determinando suspensão de cobrança até a decisão final",
"condenando a parte requerida ao pagamento de danos materiais comprovados",
"mantendo a condenação e impondo obrigação de reparar imagem",
"afastando a responsabilidade por causa excludente de ilicitude",
"anulando ato administrativo por falta de motivação",
"determinando a restituição com atualização monetária e juros legais",
"reconhecendo a nulidade do ato por ilegalidade material",
"determinando reintegração com indenização complementar",
"fixando nova dosimetria conforme guia técnico",
"ordenando reabertura e determinação de perícia complementar",
"estabelecendo obrigação de fazer e prestação de contas",
"reconhecendo a nulidade contratual por erro substancial",
"determinando suspensão da exigibilidade e instauração de procedimento administrativo",
"condenando ao pagamento de honorários periciais e sucumbenciais",
"mantendo a sentença com fundamento em súmula vinculante",
"afastando responsabilidade por ausência de elemento subjetivo",
"anulando decisão por violação de norma processual",
"determinando restituição integral e compensação de prejuízos",
"reconhecendo responsabilidade objetiva por dano ambiental",
"determinando reintegração com estabilidade provisória e indenização",
"fixando nova dosimetria e aplicando atenuantes processuais",
"ordenando reabertura e produção de prova técnica especializada",
"estabelecendo obrigação de fazer com multa diária progressiva",
"reconhecendo nulidade por simulação contratual",
"determinando suspensão da exigibilidade e bloqueio de ativos",
"condenando ao pagamento de dano emergente e lucros cessantes",
"mantendo a condenação e majorando o valor da reparação",
"afastando a responsabilidade por ausência de conduta vinculante",
"anulando ato por ausência de atribuição legal",
"determinando restituição com imposição de medidas reparatórias",
"reconhecendo a nulidade do negócio jurídico por coação",
"determinando reintegração e reintegração de função com efeitos retroativos",
"fixando nova dosimetria e aplicando regime de cumprimento especial",
"ordenando reabertura para produção de prova testemunhal complementar",
"estabelecendo obrigação de fazer e execução coercitiva",
"reconhecendo a nulidade por incapacidade relativa de parte",
"determinando suspensão da exigibilidade por irregularidade formal",
"condenando ao pagamento de multa e reparação moral",
"mantendo a condenação com aplicação de precedente regional",
"afastando a responsabilidade por caso fortuito externo e irresistível",
"anulando a sentença por omissão de fundamentação",
"determinando restituição em dobro com publicação oficial e intimação",
"reconhecendo responsabilidade civil e fixando indenização por dano moral coletivo",
"determinando reintegração com pagamento de indenização complementar",
"fixando nova dosimetria e aplicando circunstâncias atenuantes",
"ordenando reabertura e juntada de documentos novos",
"estabelecendo obrigação de fazer com termo de ajustamento de conduta",
"reconhecendo nulidade por vício no consentimento e condicionando efeitos",
"determinando suspensão da exigibilidade do débito com bloqueio administrativo",
"condenando a parte ao pagamento de custas e incidência de juros legais",
"mantendo a condenação e determinando a execução provisória",
"afastando a responsabilidade por falta de nexo jurídico",
"anulando o ato por vício insanável e determinando restituição",
"determinando restituição em dobro com cominação de multa diária",
"reconhecendo a responsabilidade solidária com imposição de obrigações alternativas",
"determinando reintegração com ressarcimento de benefícios e vantagens",
"fixando nova dosimetria e estabelecendo regime de cumprimento diferenciado",
"ordenando reabertura para esclarecimento de provas periciais",
"estabelecendo obrigação de fazer e estipulando multa compensatória",
"reconhecendo nulidade por simulação e determinando extinção do contrato",
"determinando suspensão da exigibilidade e instauração de sindicância administrativa",
"condenando a parte ao pagamento de indenização por danos coletivos",
"mantendo a condenação com fundamento em tese consolidada",
"afastando a responsabilidade em razão de força maior reconhecida",
"anulando ato por vício de notificação e determinando novo ato",
"determinando restituição com juros legais e atualização monetária",
"reconhecendo nulidade do título por irregularidade formal",
"determinando reintegração e pagamento de diferenças salariais",
"fixando nova dosimetria com remissão a precedente do tribunal superior",
"ordenando reabertura e produção de prova documental complementar",
"estabelecendo obrigação de fazer com termo de cumprimento e fiscalização",
"reconhecendo nulidade por erro essencial e declarando nulidade parcial",
"determinando suspensão da exigibilidade até decisão administrativa",
"condenando ao pagamento de multa administrativa e obrigação de reparar danos",
"mantendo a condenação com análise pormenorizada dos autos",
"afastando a responsabilidade por ausência de ilicitude aparente",
"anulando a decisão por violação ao princípio do juiz natural",
"determinando restituição integral com correção monetária e juros",
"reconhecendo nulidade por omissão de testemunha essencial",
"determinando reintegração com reintegração imediata e estabilidade",
"fixando nova dosimetria com aplicação de regime de progressão",
"ordenando reabertura por irregularidade na instrução inicial",
"estabelecendo obrigação de fazer e pagamento de multa compensatória",
"reconhecendo nulidade por fraude processual e determinando anulação",
"determinando suspensão da exigibilidade com imposição de caução",
"condenando a parte ao pagamento de indenização por danos materiais e morais",
"mantendo a condenação e determinando execução imediata",
"afastando a responsabilidade por ausência de comportamento ilícito",
"anulando o ato por incompetência funcional e remetendo ao juízo competente",
"determinando restituição com bloqueio de valores para garantia",
"reconhecendo a nulidade do acordo por vício de consentimento",
"determinando reintegração e reintegração administrativa com efeitos legais",
"fixando nova dosimetria com modulação de efeitos",
"ordenando reabertura para análise de prova técnica especializada",
"estabelecendo obrigação de fazer e multa por descumprimento progressivo",
"reconhecendo nulidade por simulação contratual e determinando ressarcimento",
"determinando suspensão da exigibilidade com remessa ao órgão fiscalizador",
"condenando ao pagamento de custas e honorários em percentual fixo",
"mantendo a condenação e determinando medidas reparatórias imediatas",
"afastando responsabilidade por falta de dolo ou culpa grave",
"anulando o ato administrativo por violação de razãoformal",
"determinando restituição com compensação entre as partes",
"reconhecendo nulidade por violação de norma de ordem pública",
"determinando reintegração com efeitos retroativos e ressarcimento",
"fixando nova dosimetria e estabelecendo penas alternativas",
"ordenando reabertura para complementação de prova pericial",
"estabelecendo obrigação de fazer com obrigação de fiscalização continuada",
"reconhecendo nulidade por erro substancial e determinação de indenização",
"determinando suspensão da exigibilidade com condicionamento à regularização",
"condenando ao pagamento de multa e aplicação de medidas administrativas",
"mantendo a condenação com imposição de obrigação de adequação",
"afastando a responsabilidade por ausência de causa eficiente",
"anulando ato por vício insanável e determinando reparação subsidiária",
"determinando restituição com imposição de medidas restauratórias",
"reconhecendo nulidade contratual e determinando rescisão amigável",
"determinando reintegração e manutenção de vínculo funcional",
"fixando nova dosimetria com modulação de efeitos no tempo",
"ordenando reabertura e designação de audiência de instrução",
"estabelecendo obrigação de fazer e regulamentação de prestação de serviço",
"reconhecendo nulidade por fraude na documentação e devolução de valores",
"determinando suspensão da exigibilidade e instauração de processo administrativo",
"condenando ao pagamento de indenização por dano moral coletivo e reparação",
"mantendo a condenação com referência a precedente vinculante",
"afastando responsabilidade por ausência de culpa consciente",
"anulando a decisão por vício de procedimento sancionatório",
"determinando restituição com correção monetária e multa reparatória",
"reconhecendo nulidade por ofensa à coisa julgada e determinando medidas",
"determinando reintegração com pagamento de vantagens e indenização",
"fixando nova dosimetria e aplicando regime de progressão de pena",
"ordenando reabertura e produção de prova pericial complementar",
"estabelecendo obrigação de fazer com prazo e fiscalização por autoridade",
"reconhecendo nulidade por coação e tornando o ato inexistente",
"determinando suspensão da exigibilidade com comunicação ao cadastro fiscal",
"condenando ao pagamento de multa e prestação de serviço comunitário",
"mantendo a condenação e determinando medidas compensatórias",
"afastando responsabilidade por ausência de comportamento antijurídico",
"anulando ato por vício de forma e determinando novo procedimento",
"determinando restituição com aplicação de juros moratórios",
"reconhecendo nulidade por lesão grave ao princípio da boa-fé contratual",
"determinando reintegração com estabilidade provisória e reintegração de direito",
"fixando nova dosimetria e aplicando critérios de proporcionalidade",
"ordenando reabertura por prova documental inusitada",
"estabelecendo obrigação de fazer e regime de penalidades graduais",
"reconhecendo nulidade por fraude e determinando responsabilização civil",
"determinando suspensão da exigibilidade e bloqueio administrativo de atos",
"condenando ao pagamento de indenização por danos estéticos",
"mantendo a condenação com imposição de medidas de reparação coletiva",
"afastando responsabilidade por ocorrência de caso fortuito de força maior",
"anulando ato por falta de fundamentação adequada",
"determinando restituição com obrigação de reparar prejuízos imediatos",
"reconhecendo nulidade por vício de vontade e determinando anulação",
"determinando reintegração com regularização de registro funcional",
"fixando nova dosimetria e aplicando regime de penas alternativas",
"ordenando reabertura e realização de perícia complementar",
"estabelecendo obrigação de fazer e regime de fiscalização continuada",
"reconhecendo nulidade por simulação e devolução de valores",
"determinando suspensão da exigibilidade e instauração de sindicância",
"condenando ao pagamento de multa administrativa e indenização por danos coletivos",
"mantendo a condenação e ordenando medidas de recomposição patrimonial",
"afastando responsabilidade por causa excludente de ilicitude reconhecida",
"anulando ato por vício formal e determinando reabertura do processo",
"determinando restituição com compensação e indenização complementar",
"reconhecendo nulidade por abuso de direito e determinando reparação",
"determinando reintegração e pagamento de diferenças salariais retroativas",
"fixando nova dosimetria e aplicando penas restritivas de direito",
"ordenando reabertura por irregularidade na instrução probatória",
"estabelecendo obrigação de fazer e multa por descumprimento reiterado",
"reconhecendo nulidade por fraude processual e decretando nulidade absoluta",
"determinando suspensão da exigibilidade e envio de relatório ao órgão fiscalizador",
"condenando ao pagamento de indenização por dano ambiental e recomposição",
"mantendo a condenação com aplicação de medidas compensatórias e reparatórias",
"afastando responsabilidade por excludente de responsabilidade civil",
"anulando ato por ausência de notificação válida e determinando nova intimação",
"determinando restituição com imposição de medidas cautelares patrimoniais",
"reconhecendo nulidade por vício substancial e revogando os efeitos",
"determinando reintegração e observância de estabilidade provisória prevista em lei",
"fixando nova dosimetria e aplicando circunstâncias atenuantes e agravantes",
"ordenando reabertura e diligência para obtenção de prova técnica",
"estabelecendo obrigação de fazer com termo de ajustamento judicial",
"reconhecendo nulidade por fraude documental e determinando reparação",
"determinando suspensão da exigibilidade e bloqueio de conta vinculada",
"condenando ao pagamento de danos materiais e lucros cessantes comprovados",
"mantendo a condenação e determinando medidas de reparação emergencial",
"afastando responsabilidade por força maior alheia à parte",
"anulando ato por ausência de competência e remetendo ao órgão competente",
"determinando restituição com aplicação de correção monetária e juros",
"reconhecendo nulidade por invalidade do negócio jurídico e declarando nulidade",
"determinando reintegração e pagamento de vantagens funcionais devidas",
"fixando nova dosimetria e impondo regime de cumprimento específico",
"ordenando reabertura e complementação de prova pericial de alta complexidade",
"estabelecendo obrigação de fazer e supervisão de cumprimento por autoridade",
"reconhecendo nulidade por simulação contratual e devolução integral",
"determinando suspensão da exigibilidade e abertura de procedimento administrativo",
"condenando ao pagamento de multa e aplicação de medidas de ressarcimento coletivo",
"mantendo a condenação com modulação de efeitos e aplicação de precedente",
"afastando responsabilidade por inexistência de conduta culposa",
"anulando o ato por vício insanável e determinando reparação subsidiária",
"determinando restituição com multa por litispendência injustificada",
"reconhecendo nulidade por contradição entre cláusulas contratuais",
"determinando reintegração com reintegração administrativa e pagamento retroativo",
"fixando nova dosimetria e aplicando critérios de razoabilidade",
"ordenando reabertura para oitiva de prova testemunhal essencial",
"estabelecendo obrigação de fazer e aplicação de medidas de contenção",
"reconhecendo nulidade por dolo e determinando anulação do negócio jurídico",
"determinando suspensão da exigibilidade e comunicação aos cadastros públicos",
"condenando ao pagamento de indenização por danos emergentes e lucros cessantes",
"mantendo a condenação com determinação de execução provisória",
"afastando responsabilidade por ausência de nexo de causalidade comprovado",
"anulando ato por irregularidade de procedimento e determinando novo ato",
"determinando restituição com imposição de tutela específica",
"reconhecendo nulidade por violação do princípio da boa-fé objetiva",
"determinando reintegração e restabelecimento de vínculo contratual",
"fixando nova dosimetria e aplicando regime de sanção alternativa",
"ordenando reabertura por vício de instrução e irregularidade no processo",
"estabelecendo obrigação de fazer e aplicação de multa progressiva",
"reconhecendo nulidade por fraude na contratação e devolução de valores",
"determinando suspensão da exigibilidade e instauração de procedimento sancionador",
"condenando ao pagamento de indenização por dano coletivo e medidas reparatórias",
"mantendo a condenação com imposição de obrigação de reparar imagem pública",
"afastando responsabilidade por caso fortuito interno",
"anulando ato por ausência de motivação suficiente e determinando reanálise",
"determinando restituição com obrigação de publicação de retratação",
"reconhecendo nulidade por erro essencial e anulando os efeitos do ato",
"determinando reintegração e pagamento de indenização complementar por danos morais",
"fixando nova dosimetria e estabelecendo medidas de reintegração social",
"ordenando reabertura para juntada de prova documental relevante",
"estabelecendo obrigação de fazer e aplicação de medidas de monitoramento",
"reconhecendo nulidade por coação e declarando inexistência do negócio",
"determinando suspensão da exigibilidade e instauração de controle administrativo",
"condenando ao pagamento de multa e reparação por danos ambientais comprovados",
"mantendo a condenação com imposição de medidas de reparação emergencial",
"afastando responsabilidade por ausência de elemento subjetivo do tipo",
"anulando o ato por vício formal e determinando correção processual",
"determinando restituição com imposição de medidas de compensação imediata",
"reconhecendo nulidade por violação de direito fundamental e determinando reparação",
"determinando reintegração com estabilidade temporária e pagamento retroativo",
"fixando nova dosimetria e aplicando regime de cumprimento adaptado",
"ordenando reabertura e produção de prova técnica especializada adicional",
"estabelecendo obrigação de fazer e aplicação de medidas de fiscalização sistemática",
"reconhecendo nulidade por fraude documental e condenando à devolução",
"determinando suspensão da exigibilidade e instauração de procedimento sancionador administrativo",
"condenando ao pagamento de indenização por dano moral e material conjugados",
"mantendo a condenação e exigindo execução imediata das medidas reparatórias",
"afastando responsabilidade por força maior devidamente comprovada",
"anulando ato por incompetência absoluta e remetendo ao juízo apropriado",
"determinando restituição com compensação e abatimento proporcional",
"reconhecendo nulidade por vício substancial e determinando perda de efeitos",
"determinando reintegração com reintegração funcional e pagamento de vantagens",
"fixando nova dosimetria e aplicando medidas de reparação administrativa",
"ordenando reabertura e designando nova audiência de instrução e julgamento",
"estabelecendo obrigação de fazer e imposição de cláusula de garantia",
"reconhecendo nulidade por simulação e ordenando ressarcimento integral",
"determinando suspensão da exigibilidade com comunicação aos órgãos competentes",
"condenando ao pagamento de multa e aplicação de medidas de recomposição patrimonial",
"mantendo a condenação com imposição de medidas de prevenção e controle",
"afastando responsabilidade por relação de causalidade não comprovada",
"anulando o ato por vício processual e determinando nova tramitação",
"determinando restituição com imposição de medidas de restituição efetiva",
"reconhecendo nulidade por ato de improbidade e determinando ressarcimento",
"determinando reintegração com estabilização provisória do vínculo empregatício",
"fixando nova dosimetria e aplicando regime de sanção alternativa educativa",
"ordenando reabertura e requisição de laudo pericial complementar",
"estabelecendo obrigação de fazer e determinação de cronograma de execução",
"reconhecendo nulidade por erro essencial na celebração do negócio",
"determinando suspensão da exigibilidade com imposição de medidas cautelares",
"condenando ao pagamento de indenização por prejuízo patrimonial e moral"
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
