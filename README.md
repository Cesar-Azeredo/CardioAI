# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto

CardioIA: A Nova Era da Cardiologia Inteligente

## Nome do grupo

Grupo Zion

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/carlos-costato/">Carlos Costato</a>
- <a href="https://www.linkedin.com/in/phellype-massarente-13739810a/">Phellype Flaibam</a>
- <a href="https://www.linkedin.com/in/cesar-azeredo">Cesar Azeredo</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Andre Godoy</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Coordenador</a>


## 📜 Descrição

O CardioIA e um projeto academico que conecta tecnologia, ciencia de dados e saude para simular o ecossistema de uma cardiologia moderna. A proposta integra dados clinicos, modelos de Machine Learning, Visao Computacional, IoT e agentes inteligentes para apoiar triagem, diagnostico, monitoramento, assistencia remota e previsoes medicas.

Esta primeira etapa corresponde a Fase 1 - Batimentos de Dados: Mapeando o Coracao Moderno. Nela, o grupo assume o papel de cientista de dados hospitalar para levantar, organizar e compreender dados cardiologicos que servirao de base para as proximas fases do projeto.

O foco da entrega e montar uma base inicial robusta com pensamento critico, considerando desde ja principios de Governanca de Dados, qualidade dos dados, vies e privacidade. A dificuldade em encontrar dados publicos, especialmente em saude, faz parte do processo real de projetos de IA. Por isso, persistencia, criatividade e combinacao de fontes (incluindo dados simulados quando necessario) sao elementos esperados nesta fase.

> Governanca de dados e vies desta entrega, com numeros medidos (nao estimados) para cada uma das quatro bases: [`document/fase-01/governanca-e-vies.md`](document/fase-01/governanca-e-vies.md).

### Objetivo geral da Entrega 1

Buscar e preparar tres tipos de dados fundamentais para uso futuro no projeto:

1. Dados numericos (simulados ou reais) relacionados a pacientes cardiacos.
2. Dados textuais medicos ou literarios relacionados a saude cardiovascular.
3. Dados visuais medicos representando exames ou sinais do coracao.

### Mapa mental da jornada (7 fases)

Referencia apresentada no enunciado:

- mapaMental - CardioIA_ A Nova Era da Cardiologia Inteligente.svg

## ✅ Escopo da Entrega 1 (Fase 1)

### Parte 1 - Dados Numericos (IoT)

- Montar dataset com minimo de 100 linhas.
- Incluir variaveis como: idade, sexo, pressao arterial, colesterol, historico cardiaco, sintomas, frequencia cardiaca, entre outras.
- Disponibilizar link publico para os dados completos (OneDrive, Google Drive ou similar).
- Explicar no README a origem dos dados (reais ou simulados).
- Justificar as variaveis clinicamente mais relevantes para IA em saude.

**Entregue**: UCI Heart Disease, base Cleveland — dado real (nao simulado), 303 pacientes, licenca CC BY 4.0. Variaveis mais relevantes clinicamente: tipo de dor toracica, frequencia cardiaca maxima, depressao do segmento ST, numero de vasos por fluoroscopia (maior poder discriminativo nesta base), alem dos fatores de risco classicos (idade, sexo, colesterol, pressao em repouso). Justificativa individual de cada variavel e as decisoes de tratamento (auséncias preservadas, alvo em duas formas) em [`document/fase-01/dados-numericos.md`](document/fase-01/dados-numericos.md). Dados completos (CSV + XLSX) tambem no [Google Drive](https://drive.google.com/drive/folders/1eTMQ1dnlVJRoTAAd39kqipLyDX-iuLCB?usp=drive_link).

### Parte 2 - Dados Textuais (NLP)

- Baixar no minimo 2 textos em formato .txt sobre doencas cardiacas, saude publica, sintomas ou tratamentos.
- Usar fontes confiaveis, como SciELO, BVS, SUS ou Projeto Gutenberg.
- Armazenar os textos em subpasta do repositorio (assets ou docs/document).
- Explicar como os textos poderao ser usados em NLP:
    - analise de sentimentos
    - extracao de sintomas
    - classificacao de topicos
- Justificar relevancia dessas analises no contexto de IA aplicada a saude.

**Entregue**: 2 textos em `assets/textos/` — um tecnico-cientifico (SciELO, Arquivos Brasileiros de Cardiologia, 1.608 palavras, CC BY-NC 3.0) e um de comunicacao em saude publica (Ministerio da Saude, 858 palavras, CC BY-ND 3.0). O contraste de registro entre os dois e o proprio exemplo do problema que a Fase 5 (chatbot) precisa resolver: traduzir termo clinico para linguagem de paciente. Analise de sentimento nao se aplica a nenhum dos dois (nenhum e relato de paciente) — o corpus serve de baseline de vocabulario. Detalhe das 3 tecnicas de NLP com exemplo real de cada texto em [`document/fase-01/dados-textuais.md`](document/fase-01/dados-textuais.md). Textos disponiveis tanto versionados em `assets/textos/` quanto no [Google Drive](https://drive.google.com/drive/folders/1IKF4nawS7BT8J5obI0AqoAviMeqFcsh1?usp=drive_link).

### Parte 3 - Dados Visuais (Visao Computacional)

- Reunir no minimo 100 imagens (.jpg ou .png) de exames cardiologicos (ECG, angiograma, raio-X toracico etc.).
- Disponibilizar link publico para o conjunto completo de imagens.
- Explicar possibilidades de analise por Visao Computacional:
    - deteccao de padroes
    - identificacao de bordas
    - reconhecimento de anomalias
- Destacar importancia dessas analises para solucoes de IA em saude.

**Entregue**: ECG Images dataset of Cardiac Patients v2 (Mendeley Data, CC BY 4.0). Do dataset completo (928 arquivos), apenas 491 sao imagens de conteudo unico por hash MD5 (47% de redundancia, medida nao estimada) — deduplicado antes de qualquer amostragem. Selecao final: 120 imagens, balanceadas 30/30/30/30 por categoria, semente fixa, sem recompressao. Justificativa de deteccao de bordas/padroes/anomalias e o achado de *shortcut learning* (hash raso confundiu template do aparelho com conteudo clinico) em [`document/fase-01/dados-visuais.md`](document/fase-01/dados-visuais.md). Conjunto completo de 120 imagens no [Google Drive](https://drive.google.com/drive/folders/12YhReksoB8K-aWQsubtUIaEx4zK9EuF3?usp=drive_link).

## 📦 Entregaveis obrigatorios

O repositorio deve conter:

1. README.md detalhado com descricao da fase, objetivos, fontes e justificativas das tres partes.
2. Subpasta com conteudos textuais (assets e/ou document).
3. Links publicos acessiveis com os conjuntos completos de dados numericos e visuais.

Status: os 3 itens entregues (documentacao completa em `document/fase-01/`; textos em `assets/textos/`; links publicos na secao "Links publicos da Entrega 1" acima).

## ⚠️ Orientacoes importantes da atividade

- Verificar o arquivo antes do upload final (nao e possivel reenviar apos fechamento/correcao).
- Nao deixar envio para os ultimos minutos do prazo.
- Nao compartilhar respostas em grupos para evitar plagio.
- Prazo de ate 15 dias apos publicacao da nota para solicitar revisao.

## 🧭 Boas praticas para esta fase

- Priorizar fontes eticas e legais para dados de saude.
- Registrar claramente se os dados sao reais, anonimizados ou simulados.
- Organizar desde ja a estrutura para notebooks futuros (Colab/Jupyter).
- Manter padrao de nomes e versionamento dos arquivos de dados.

## 📊 Criterios de avaliacao (10 pontos)

1. Dataset numerico entregue corretamente, organizado e explicado - 3 pontos.
2. Textos selecionados e contextualizados corretamente - 2 pontos.
3. Imagens entregues e bem justificadas em seu potencial para analise por IA - 2 pontos.
4. Documento resumo com explicacoes claras, objetivas e bem estruturadas - 2 pontos.
5. Cumprimento das orientacoes gerais e prazo de entrega - 1 ponto.

## 🗂 Organização dos dados da Entrega 1

Organizacao adotada (dentro do padrao atual do template, sem pastas novas na raiz):

- assets/textos/ -> arquivos .txt da Parte 2 (NLP)
- assets/imagens/amostras/ -> ~12 imagens de amostra da Parte 3; conjunto completo hospedado externamente (ver assets/imagens/LEIA-ME.md)
- assets/mapa-mental/ -> SVG/PNG do mapa mental da jornada de 7 fases
- document/datasets/raw/ e document/datasets/processed/ -> dataset numerico (Parte 1), bruto e tratado (.csv e .xlsx)
- document/datasets/README.md -> proveniencia (fonte, URL, DOI, licenca, data de acesso) das tres bases
- document/fase-01/ -> documentos tecnicos da fase (dados numericos, textuais, visuais, governanca e vies)
- document/ai_project_document_fiap.md -> documento resumo avaliado pela rubrica
- links publicos no README -> dados completos (numericos e visuais)

## 🔗 Links publicos da Entrega 1

Pasta-mae com todo o conteudo da Fase 1 no Google Drive:
[CardioIA - Fase 1](https://drive.google.com/drive/folders/1kKpAlFfaA06UMaPxirurEwRaDQi6ySbg?usp=drive_link)

- **Dataset numerico — CSV e XLSX** (303 linhas, os dois formatos na mesma pasta):
  [Google Drive](https://drive.google.com/drive/folders/1eTMQ1dnlVJRoTAAd39kqipLyDX-iuLCB?usp=drive_link)
- **Imagens** (120 selecionadas, ~76 MB):
  [Google Drive](https://drive.google.com/drive/folders/12YhReksoB8K-aWQsubtUIaEx4zK9EuF3?usp=drive_link)
- **Fontes textuais (.txt)**: disponiveis de duas formas — versionadas neste repositorio em `assets/textos/`, e tambem no
  [Google Drive](https://drive.google.com/drive/folders/1IKF4nawS7BT8J5obI0AqoAviMeqFcsh1?usp=drive_link) (util para quem preferir baixar sem clonar o repositorio).


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.
  - <b>assets/textos/</b>: os 2 arquivos `.txt` da Parte 2 (NLP).
  - <b>assets/imagens/amostras/</b>: ~12 imagens de amostra da Parte 3 (o conjunto completo de 120 fica hospedado externamente — ver `assets/imagens/LEIA-ME.md`).
  - <b>assets/mapa-mental/</b>: SVG/PNG do mapa mental da jornada de 7 fases.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto. Não usado na Fase 1; reservado para parâmetros de sensores simulados (Fase 3) e de modelos preditivos (Fase 6).

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.
  - <b>document/datasets/</b>: dataset numérico bruto e tratado (`raw/`, `processed/`), dicionário de dados e tabela de proveniência das quatro bases.
  - <b>document/fase-01/</b>: documentação técnica da Fase 1 — dados numéricos, textuais, visuais, governança e viés, e autoavaliação contra a rubrica.

- <b>notebooks</b>: notebooks de EDA/exploração, organizados por fase (`notebooks/fase-01/` reservado para a Fase 1).

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.
  - <b>scripts/fase-01/</b>: os 5 scripts reprodutíveis desta entrega (coleta, perfilamento e tratamento do dataset numérico, preparação dos textos, organização das imagens) — ver "Como executar o código" abaixo.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

**Pré-requisitos**: Python 3.12 (versão travada para paridade com o runtime do Google Colab — ver seção 7 do `CLAUDE.md`/`AGENTS.md`).

```bash
# 1. Criar e ativar um ambiente virtual
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Instalar as dependências travadas
pip install -r requirements.txt
```

**Fase 1 — Batimentos de Dados**, nesta ordem:

```bash
# Parte 1 — dataset numérico (UCI Heart Disease)
python scripts/fase-01/01_coleta_dataset_numerico.py
python scripts/fase-01/02_perfila_dataset_numerico.py
python scripts/fase-01/03_trata_dataset_numerico.py

# Parte 2 — textos (SciELO + Ministério da Saúde)
python scripts/fase-01/04_prepara_textos.py

# Parte 3 — imagens de ECG (Mendeley Data)
# pré-requisito: dataset já baixado e descompactado fora do repositório
# (ver cabeçalho do script para o caminho esperado)
python scripts/fase-01/05_organiza_imagens.py
```

Cada script imprime um relatório da execução (contagens, validações,
decisões aplicadas) e é idempotente — pode ser rodado de novo sem
efeito colateral. Detalhe de cada etapa em `document/fase-01/`.


## 🗃 Histórico de lançamentos

* 0.5.0 - XX/XX/2024
    * 
* 0.4.0 - XX/XX/2024
    * 
* 0.3.0 - XX/XX/2024
    * 
* 0.2.0 - XX/XX/2024
    * 
* 0.1.0 - 27/08/2026
    * Fase 1 — Batimentos de Dados: dataset numérico (UCI Heart Disease, 303 pacientes), corpus textual (2 textos, técnico + leigo) e conjunto de imagens de ECG (120 selecionadas de 928, deduplicadas) coletados, tratados e documentados, com governança de dados e viés registrados.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


