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

### Parte 2 - Dados Textuais (NLP)

- Baixar no minimo 2 textos em formato .txt sobre doencas cardiacas, saude publica, sintomas ou tratamentos.
- Usar fontes confiaveis, como SciELO, BVS, SUS ou Projeto Gutenberg.
- Armazenar os textos em subpasta do repositorio (assets ou docs/document).
- Explicar como os textos poderao ser usados em NLP:
    - analise de sentimentos
    - extracao de sintomas
    - classificacao de topicos
- Justificar relevancia dessas analises no contexto de IA aplicada a saude.

### Parte 3 - Dados Visuais (Visao Computacional)

- Reunir no minimo 100 imagens (.jpg ou .png) de exames cardiologicos (ECG, angiograma, raio-X toracico etc.).
- Disponibilizar link publico para o conjunto completo de imagens.
- Explicar possibilidades de analise por Visao Computacional:
    - deteccao de padroes
    - identificacao de bordas
    - reconhecimento de anomalias
- Destacar importancia dessas analises para solucoes de IA em saude.

## 📦 Entregaveis obrigatorios

O repositorio deve conter:

1. README.md detalhado com descricao da fase, objetivos, fontes e justificativas das tres partes.
2. Subpasta com conteudos textuais (assets e/ou document).
3. Links publicos acessiveis com os conjuntos completos de dados numericos e visuais.

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

Preencher quando os dados estiverem prontos:

- Dataset numerico (CSV/XLSX):
- Imagens (JPG/PNG):
- Fontes textuais (.txt):


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

*Acrescentar as informações necessárias sobre pré-requisitos (IDEs, serviços, bibliotecas etc.) e instalação básica do projeto, descrevendo eventuais versões utilizadas. Colocar um passo a passo de como o leitor pode baixar o seu código e executá-lo a partir de sua máquina ou seu repositório. Considere a explicação organizada em fase.*


## 🗃 Histórico de lançamentos

* 0.5.0 - XX/XX/2024
    * 
* 0.4.0 - XX/XX/2024
    * 
* 0.3.0 - XX/XX/2024
    * 
* 0.2.0 - XX/XX/2024
    * 
* 0.1.0 - XX/XX/2024
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


