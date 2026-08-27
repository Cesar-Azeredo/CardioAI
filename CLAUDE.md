# CLAUDE.md — Contexto operacional do projeto CardioIA

> **Este arquivo e o `AGENTS.md` na raiz têm conteúdo idêntico.**
> `CLAUDE.md` é lido pelo Claude Code; `AGENTS.md` é lido pelo GitHub Copilot, Cursor, Codex e afins.
> **Se você alterar um, replique a alteração no outro na mesma tarefa.** Não deixe os dois divergirem.

---

## 1. O que é este projeto

**CardioIA — A Nova Era da Cardiologia Inteligente.**
Projeto acadêmico do curso de Inteligência Artificial da **FIAP**, conduzido pelo método **PBL (Project Based Learning)**. O objetivo é construir, ao longo de **7 fases**, uma plataforma digital que simule o ecossistema de uma cardiologia moderna, integrando dados clínicos, Machine Learning, Visão Computacional, IoT, NLP e agentes inteligentes.

Contexto que justifica o projeto (usar nas justificativas dos documentos): doenças cardiovasculares são a principal causa de morte no mundo, com aproximadamente **17,9 milhões de óbitos anuais**; infartos, arritmias, insuficiência cardíaca e AVCs são comuns e podem ser prevenidos com diagnóstico precoce.

### Regra estrutural mais importante

**Este é um monorepo incremental.** Cada fase é uma entrega avaliada separadamente, mas **todas vivem no mesmo repositório e as fases posteriores consomem os artefatos das anteriores**.

Consequências práticas, que valem como regra:

- **Nunca apague, renomeie ou reescreva artefatos de fases já entregues.** As fases são **aditivas**.
- **Nunca organize o repositório como "uma pasta isolada por fase".** Organize por **função** (`data/`, `docs/`, `notebooks/`, `scripts/`, `src/`) e use subpastas por fase **dentro** dessas pastas. Motivo: a Fase 2 vai treinar modelos sobre o CSV da Fase 1, a Fase 4 vai processar as imagens da Fase 1 e a Fase 5 vai usar os textos da Fase 1. Duplicar dado por fase quebra isso.
- Ao iniciar uma fase nova, **leia primeiro o que as fases anteriores produziram** antes de escrever qualquer código.

---

## 2. Estado atual

| Campo | Valor |
|---|---|
| **Fase em andamento** | **Fase 1 — Batimentos de Dados** |
| Fases concluídas | nenhuma |
| Ambiente | VS Code local, repositório já criado a partir do template FIAP e conectado ao GitHub |
| Idioma dos entregáveis | **Português do Brasil** |

> **Mantenha esta tabela atualizada.** Ao concluir uma fase, mova-a para "concluídas" e atualize a fase em andamento. Este é o primeiro lugar que qualquer agente olha.

---

## 3. Estrutura de diretórios

Esta árvore parte do **template FIAP** já existente no repositório (não substitui nada dele). `[F1]` = criado/preenchido na Fase 1; `[futuro]` = reservado para próximas fases; `[template]` = já existia antes da Fase 1 e permanece como está.

```
CardioIA/
├── AGENTS.md                          # este arquivo                         [F1]
├── CLAUDE.md                          # cópia idêntica deste arquivo         [F1]
├── README.md                          # ENTREGÁVEL AVALIADO — template FIAP  [F1]
├── requirements.txt                                                          [F1]
├── .gitignore                                                                [F1]
│
├── assets/
│   ├── logo-fiap.png                                                    [template]
│   ├── mapa-mental/                   # SVG/PNG do mapa mental da jornada    [F1]
│   ├── textos/                        # ENTREGÁVEL: os .txt para NLP         [F1]
│   └── imagens/
│       ├── amostras/                  # ~12 imagens leves p/ ilustrar README [F1]
│       └── LEIA-ME.md                 # explica que o conjunto está no Drive [F1]
│
├── config/                            # parâmetros de sensores (ESP32) e modelos
│   └── readme.md                                          [futuro: fase-03, fase-06]
│
├── document/
│   ├── ai_project_document_fiap.md    # DOCUMENTO RESUMO AVALIADO (rubrica)   [F1]
│   ├── datasets/
│   │   ├── raw/                       # dado como baixado, sem tratamento     [F1]
│   │   ├── processed/                 # dataset final .csv e .xlsx            [F1]
│   │   ├── dicionario-de-dados.md     # variável, tipo, unidade, faixa        [F1]
│   │   └── README.md                  # proveniência: fonte, licença, DOI...  [F1]
│   ├── fase-01/
│   │   ├── dados-numericos.md                                                 [F1]
│   │   ├── dados-textuais.md                                                  [F1]
│   │   ├── dados-visuais.md                                                   [F1]
│   │   └── governanca-e-vies.md                                               [F1]
│   ├── fase-02/ ... fase-07/                                            [futuro]
│   └── other/
│       └── readme.md                                                    [template]
│
├── notebooks/
│   ├── fase-01/                       # EDA do dataset numérico              [F1]
│   └── fase-02/ ...                                                     [futuro]
│
├── scripts/
│   ├── readme.md                                                        [template]
│   └── fase-01/                       # coleta, tratamento, validação        [F1]
│
└── src/
    ├── readme.md                                                        [template]
    └── cardioia/                      # código reutilizável entre fases  [futuro]
```

Regras sobre a estrutura:

- Toda pasta versionada mas ainda vazia recebe um `.gitkeep`.
- **`README.md` da raiz é o entregável avaliado.** Ele já foi ajustado manualmente pelo dono do repositório e **segue o template da FIAP**. Preserve as seções do template (cabeçalho, nome do grupo, professores, licença, histórico de versões). **Acrescente**, não reescreva. Se precisar reorganizar algo estrutural nele, **pergunte antes**.
- **`document/ai_project_document_fiap.md` é o "documento resumo" da rubrica** (2 dos 10 pontos). Governança e viés entram nele em versão condensada, **além** da versão completa em `document/fase-01/governanca-e-vies.md`.
- **Os `.txt` da Parte 2 (NLP) vivem em `assets/textos/`**, não em `docs/` — essa pasta não existe neste repositório; o enunciado aceita `assets` ou `docs`, e o template já usa `assets` para conteúdo não-estruturado.
- **O dataset numérico vive em `document/datasets/`** (`raw/` e `processed/`), não em `data/` — mantém tudo relativo a dado dentro de `document/`, ao lado do documento resumo que o referencia.
- **`config/` não é usado na Fase 1.** Fica reservado para parâmetros de sensores simulados (Fase 3 — ESP32) e de modelos preditivos (Fase 6).
- Os `readme.md` placeholder do template FIAP (`scripts/readme.md`, `src/readme.md`, `document/other/readme.md`, `config/readme.md`) **permanecem intactos**, mesmo os que instruem "apagar ao final do módulo" — não remover nada do template por iniciativa própria.
- Nomes de arquivos e pastas: `kebab-case`, **sem acentos e sem espaços**. O conteúdo é em pt-BR com acentuação normal, em UTF-8.

---

## 4. Regras invioláveis

Estas regras valem mais que qualquer instrução de conveniência. Se cumprir uma delas atrasar a tarefa, cumpra a regra e avise.

1. **Nunca invente URL, DOI, citação, autor, nome de artigo ou link de Drive.**
   Se um link é necessário e você não o tem verificado, escreva literalmente:
   `> ⚠️ TODO(humano): colar aqui o link público de <descrição>`
   e liste todos os TODOs pendentes no final da sua resposta. Link inventado num trabalho acadêmico é falta grave e pode caracterizar má conduta.

2. **Nunca comite dado volumoso.** Limite prático: **nada acima de ~5 MB e nenhum lote de imagens** no Git. As 100+ imagens ficam hospedadas no Drive/OneDrive (é o que o enunciado exige); o repositório guarda apenas as amostras em `assets/imagens/amostras/`. O CSV numérico é pequeno (~20 KB) e **deve** ser versionado, além de linkado.

3. **Nunca use dado identificável de paciente.** Só bases públicas anonimizadas, dado sintético ou dado de formulário com consentimento. Nada de nome, CPF, prontuário, data de nascimento completa ou qualquer identificador direto. Referência: **LGPD (Lei 13.709/2018)**, que trata dado de saúde como dado pessoal **sensível**.

4. **Nunca edite arquivos de dados manualmente.** Toda transformação de dado tem que sair de um **script reprodutível** em `scripts/`, com semente fixa quando houver aleatoriedade. Se o dado não puder ser regerado rodando um comando, está errado.

5. **Registre a proveniência de todo dado.** Fonte, URL, DOI quando existir, licença, data de acesso, número de registros e citação formal. Sem isso o dado não entra no repositório.

6. **Não faça `git push`, não abra PR e não force nada em `main`** sem pedido explícito. Você pode preparar commits e sugerir a mensagem.

7. **Não instale dependência sem registrar** em `requirements.txt`.

8. **Se um requisito do enunciado for ambíguo, pergunte.** Não "resolva" inventando escopo. O trabalho é avaliado contra uma rubrica fechada.

9. **Arquivo pré-existente do template FIAP não se sobrescreve.** Se um arquivo do template (`.gitignore`, `.gitattributes`, `README.md`, `ai_project_document_fiap.md`, os `readme.md` de pasta, `.github/`) precisar mudar, **preserve o conteúdo original e estenda** com o mínimo necessário. Convenção do template é decisão da instituição até prova em contrário — se ela parecer conflitar com o pedido, **pare e pergunte antes de alterar**. Ao alterar um desses arquivos, anuncie a mudança em destaque na resposta.

---

## 5. Fase 1 — Batimentos de Dados

**Papel assumido:** cientista de dados hospitalar. A missão é levantar, organizar e entender dados cardiológicos que vão alimentar os módulos inteligentes das fases seguintes — com atenção explícita a **Governança de Dados** e **viés**.

### 5.1 Requisitos literais do enunciado

**Parte 1 — Dados numéricos (IoT)**
- Dataset com **mínimo de 100 linhas**.
- Formato **obrigatoriamente `.csv` ou `.xlsx`**.
- Variáveis do tipo: idade, sexo, pressão arterial, colesterol, histórico de doença cardíaca, sintomas, frequência cardíaca etc.
- No `README.md`: link para os dados hospedados em serviço público (Drive/OneDrive), explicação clara da **origem** (real ou simulado) e destaque das **variáveis mais relevantes do ponto de vista clínico, com justificativa** do porquê importam para um projeto de IA em saúde.

**Parte 2 — Dados textuais (NLP)**
- **No mínimo 2 arquivos `.txt`** sobre doenças cardíacas, saúde pública, sintomas ou tratamentos.
- Fontes sugeridas pelo enunciado: **SciELO, BVS, artigos do SUS/Ministério da Saúde, ou literatura clássica via Projeto Gutenberg**.
- Ficam em subpasta **`docs`** ou **`assets`** → neste repositório: **`docs/textos/`**.
- No `README.md`: explicar como esses textos podem ser explorados por algoritmos de NLP (ex.: análise de sentimentos, extração de sintomas, classificação de tópicos) e **justificar a relevância** para IA em saúde.

**Parte 3 — Dados visuais (VC)**
- **No mínimo 100 imagens** `.jpg` ou `.png` de **um tipo** de exame cardiológico (ECG, angiograma ou raio-X torácico).
- Link público para o conjunto hospedado (Drive/OneDrive).
- No `README.md`: justificar como as imagens poderão ser analisadas por Visão Computacional (ex.: detecção de padrões, identificação de bordas, reconhecimento de anomalias) e a importância disso para IA em saúde.

**Entregáveis**
- `README.md` detalhado explicando o projeto, descrevendo as três partes e indicando objetivos e fontes.
- Subpasta `docs` ou `assets` com conteúdo.
- **Links públicos acessíveis a qualquer pessoa** — o time da FIAP precisa abrir sem pedir permissão. Testar em janela anônima.

### 5.2 Rubrica de avaliação (10 pontos) — otimizar contra isto

| Critério | Pontos |
|---|---|
| Parte 1 — Dataset numérico entregue corretamente, organizado e explicado | **3** |
| Parte 2 — Textos selecionados e contextualizados corretamente | **2** |
| Parte 3 — Imagens entregues e bem justificadas em seu potencial para análise por IA | **2** |
| Documento resumo com explicações claras, objetivas e bem estruturadas | **2** |
| Cumprimento das orientações gerais e prazo de entrega | **1** |

Leitura da rubrica: **4 dos 10 pontos são de escrita e organização** (o critério de 2 pontos do documento resumo + boa parte dos critérios de cada parte, que exigem "explicado", "contextualizado", "bem justificado"). Ou seja, **texto bem-feito vale tanto quanto dado coletado**. Justificativa genérica derruba nota mesmo com dado perfeito. Toda justificativa precisa amarrar em **relevância clínica** e **uso concreto nas fases seguintes**.

### 5.3 Fontes verificadas (usar estas; não substituir por links inventados)

**Numérico — UCI Heart Disease**
- Página: `https://archive.ics.uci.edu/dataset/45/heart+disease`
- CSV direto: `https://archive.ics.uci.edu/static/public/45/data.csv`
- Via Python: `pip install ucimlrepo` → `fetch_ucirepo(id=45)`
- 303 instâncias (base Cleveland), 13 atributos + alvo `num` (0 = ausência, 1–4 = presença). Há valores faltantes.
- Licença **CC BY 4.0**. DOI `10.24432/C52P4X`.
- Citação: Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1989). *Heart Disease* [Dataset]. UCI Machine Learning Repository.
- Atende o mínimo de 100 linhas com folga (303).

**Visual — ECG Images dataset of Cardiac and COVID-19 Patients (Mendeley Data)**
- Página: `https://data.mendeley.com/datasets/gwbz3fsgp8/2` — DOI `10.17632/gwbz3fsgp8.2`
- 1.937 registros distintos de pacientes, ECG de 12 derivações, capturados com equipamento EDAN SERIES-3 em unidades de cardiologia e isolamento no Paquistão (Ch. Pervaiz Elahi Institute of Cardiology, Multan).
- Revisão manual por médicos em 5 categorias: COVID-19, batimento cardíaco anormal, infarto do miocárdio (IM), histórico prévio de IM e pessoa normal.
- Artigo descritor: Khan, A. H., Hussain, M., & Malik, M. K. (2021). *ECG images dataset of Cardiac and COVID-19 patients*. Data in Brief, 34, 106762. DOI `10.1016/j.dib.2021.106762`.
- ⚠️ **Confirmar a licença na página do dataset antes de redistribuir** e registrar a licença encontrada em `data/README.md`. O artigo descritor é CC BY-NC-ND, o que restringe obra derivada — para uso acadêmico com atribuição está adequado, mas a licença precisa estar documentada.
- Atende o mínimo de 100 imagens com muita folga. **Selecionar um subconjunto de ~120 imagens** balanceado entre as categorias disponíveis, e documentar o critério da amostragem.

**Textual — escolher no mínimo 2**
- SciELO Brasil (`https://www.scielo.br`) — buscar em *Arquivos Brasileiros de Cardiologia*; artigos em acesso aberto.
- BVS / Biblioteca Virtual em Saúde (`https://bvsalud.org`).
- Ministério da Saúde / SUS — publicações e cadernos de atenção básica sobre hipertensão e doenças cardiovasculares.
- Projeto Gutenberg (`https://www.gutenberg.org`) — domínio público, útil para um texto de perfil histórico/literário que contraste com o texto técnico.
- ⚠️ **O agente não deve fabricar título, autor ou URL de artigo.** Deixar TODO para o humano colar o link e, ao receber o link, extrair o texto, salvar como `.txt` em UTF-8 e registrar a proveniência.

Sugestão de composição que rende na rubrica: **um texto técnico-científico** (SciELO/BVS) + **um texto de comunicação em saúde pública** (Ministério da Saúde). O contraste de registro linguístico entre os dois é argumento forte na justificativa de NLP — permite comparar vocabulário técnico vs. leigo, o que é exatamente o problema da Fase 5 (chatbot que precisa traduzir termo clínico para o paciente).

### 5.4 Governança de dados e viés — obrigatório documentar

O enunciado cobra explicitamente os conceitos iniciais de Governança de Dados e de viés. Cobrir em `docs/fase-01/governanca-e-vies.md`:

- **Proveniência e licença** de cada uma das três bases, com data de acesso.
- **Finalidade** do uso (acadêmico, sem aplicação clínica real) e um aviso claro de que nada aqui serve para decisão médica.
- **LGPD**: dado de saúde é dado pessoal sensível; como a anonimização das bases públicas endereça isso.
- **Viés identificado, de forma concreta e quantificada.** Não escrever "pode haver viés"; medir e nomear. Nas bases escolhidas há vieses reais e verificáveis:
  - *UCI/Cleveland*: coleta de **1989**, hospital único nos EUA, forte desbalanceamento por sexo, faixa etária concentrada, valores faltantes em atributos como `ca` e `thal`. Um modelo treinado nisso não generaliza para a população brasileira de 2026.
  - *ECG Images*: coleta em **um único país (Paquistão)** com **um único modelo de equipamento**. O modelo pode aprender a assinatura visual do aparelho em vez da patologia — problema clássico de *shortcut learning* em imagem médica.
- **Consequência clínica do viés**: um falso negativo em triagem cardiológica é um paciente mandado para casa infartando. Assimetria de custo entre os tipos de erro precisa estar escrita.
- **Mitigações propostas** para as fases seguintes: estratificação por sexo e faixa etária, métricas por subgrupo, validação externa, e não usar acurácia global como métrica única.

### 5.5 Definition of Done da Fase 1

Só considerar a fase pronta quando **todos** os itens estiverem verdadeiros:

- [ ] Dataset em `data/processed/` em `.csv` **e** `.xlsx`, com **≥ 100 linhas** (contagem verificada por script, não estimada).
- [ ] `data/dicionario-de-dados.md` com variável, tipo, unidade, faixa válida e significado clínico de cada coluna.
- [ ] Script reprodutível de coleta/tratamento em `scripts/fase-01/`, rodando de ponta a ponta sem erro em ambiente limpo.
- [ ] **≥ 2** arquivos `.txt` em `docs/textos/`, em UTF-8, com proveniência registrada.
- [ ] **≥ 100** imagens organizadas e hospedadas, com `manifest.csv` (nome do arquivo, categoria, dimensões, origem) versionado no repositório.
- [ ] ~12 imagens de amostra em `assets/imagens/amostras/`.
- [ ] Links públicos testados **em janela anônima** e funcionando sem login.
- [ ] `README.md` da raiz cobrindo as três partes, com as justificativas clínicas e de IA exigidas, e integrado ao template FIAP sem quebrá-lo.
- [ ] `docs/fase-01/governanca-e-vies.md` completo.
- [ ] Nenhum TODO de link pendente.
- [ ] Autoavaliação escrita contra a rubrica da seção 5.2, critério por critério.

---

## 6. Roadmap das fases 2 a 7

Referência para não tomar decisão na Fase 1 que atrapalhe depois.

| Fase | Título | Escopo | Consome da Fase 1 |
|---|---|---|---|
| **2** | Diagnóstico Automatizado — IA no Estetoscópio Digital | Modelos de IA para identificar risco de doença; classificadores supervisionados; reflexão sobre responsabilidade da IA na medicina | **dataset numérico** |
| **3** | Monitoramento Contínuo — IoT no Peito do Paciente | Simulação de wearable médico com sensores **ESP32** em tempo real; dashboard de apresentação | esquema de variáveis (FC, PA) |
| **4** | Coração em Imagens — Diagnóstico com Visão Computacional | Sistema para interpretar imagens de exames; treinar modelos para detectar alterações suspeitas; módulos de visualização | **conjunto de imagens** |
| **5** | Suporte Digital ao Paciente — Assistente Cardiológico Virtual | Chatbot para acompanhamento domiciliar; NLP; discussão de ética e empatia no atendimento virtual | **corpus textual** |
| **6** | Coração Sob Controle — Previsão de Crises com IA | Sistema preditivo de eventos cardíacos por **séries temporais**; prever picos de risco; protocolos de emergência | dataset + dados do wearable |
| **7** | CardioIA — Plataforma de Inteligência Cardíaca Total | Integração de todos os módulos numa plataforma funcional; foco em usabilidade, fluxo de informação e arquitetura final | tudo |

Implicações para decisões tomadas agora:

- A escolha de **ECG** como tipo de exame na Fase 1 amarra a Fase 4. ECG é boa escolha: é imagem de sinal, com padrão geométrico regular, o que facilita tanto detecção de bordas quanto CNN, e conversa diretamente com o wearable ESP32 da Fase 3.
- O `manifest.csv` das imagens com rótulo por categoria é o que vai permitir treino supervisionado na Fase 4 sem retrabalho. Fazer isso bem agora economiza dias depois.
- Manter as variáveis de frequência cardíaca e pressão arterial bem documentadas em unidades explícitas, porque a Fase 3 vai gerar leituras que precisam ser compatíveis com esse esquema.

---

## 7. Convenções técnicas

**Stack:** Python 3.12, `pandas`, `numpy`, `matplotlib`, `openpyxl`, `ucimlrepo`, `Pillow`. Notebooks compatíveis com **Jupyter e Google Colab**. Não adicionar dependência pesada sem necessidade.

**Versão do Python travada em 3.12** — paridade com o runtime padrão do Google Colab (3.12.13 à data de escrita, com `numpy` 2.0.2, PyTorch 2.11, TensorFlow 2.20). Isso importa a partir da Fase 4 (Visão Computacional), quando o projeto passa a depender de TensorFlow/PyTorch e qualquer notebook rodado localmente precisa continuar compatível com o que roda no Colab.

**Encoding:** UTF-8 em tudo. CSV com separador `,` e decimal `.`.

**Commits:** Conventional Commits com escopo de fase, descrição em pt-BR, imperativo:

```
feat(fase-01): adiciona dataset numerico tratado em csv e xlsx
docs(fase-01): documenta governanca de dados e vies das bases
chore: cria estrutura de pastas para as sete fases
```

Commits pequenos e temáticos. Não juntar coleta de dado, documentação e estrutura no mesmo commit.

**Branches:** `main` protegida na prática. Trabalho em `fase-01/<assunto>`, integrado via PR.

**Notebooks:** limpar outputs antes de commitar.

---

## 8. Trabalho em grupo

O repositório é compartilhado por uma equipe; quem escreveu este arquivo deu o start.

- Um documento gera um dono. Antes de reescrever seção de documento que não é da tarefa atual, **pergunte**.
- Não faça refactor amplo por iniciativa própria: conflito de merge em trabalho de grupo custa mais que o ganho estético.
- `README.md` da raiz é o arquivo de maior contenção. Alterações nele: cirúrgicas e anunciadas.

---

## 9. Checklist antes de encerrar qualquer tarefa

1. Cumpri as regras invioláveis da seção 4?
2. Todo dado novo tem proveniência, licença e data de acesso registradas?
3. Todo link que eu não verifiquei está marcado como `TODO(humano)` e listado na minha resposta?
4. Alterei `AGENTS.md` ou `CLAUDE.md`? Se sim, os dois estão idênticos?
5. Se a fase avançou de estado, atualizei a tabela da seção 2?
6. Listei explicitamente o que ficou pendente para o humano fazer?
