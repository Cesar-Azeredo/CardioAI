# Autoavaliação — Fase 1, contra a rubrica (seção 5.2 do CLAUDE.md/AGENTS.md)

Autoavaliação crítica, critério por critério. Onde a nota provável não é
"cheia", digo por quê — o objetivo é identificar risco real antes da
correção, não validar o próprio trabalho.

## 1. Dataset numérico entregue corretamente, organizado e explicado — 3 pontos

**Entregue**: UCI Heart Disease (Cleveland), 303 linhas, `.csv` e `.xlsx` em
`document/datasets/processed/`, dicionário completo com legenda de código
extraída da fonte oficial (`document/datasets/dicionario-de-dados.md`),
script reprodutível de ponta a ponta (`01`, `02`, `03` em `scripts/fase-01/`),
decisões de tratamento justificadas com raciocínio explícito (ausência
preservada por ser MNAR, alvo em duas formas, faixas de sanidade separadas
de critério clínico). Variáveis mais relevantes justificadas individualmente
em `document/fase-01/dados-numericos.md`.

**Atualização**: o link público (Google Drive) foi publicado e está no
`README.md` e em `document/datasets/README.md`. Critério fechado — nada
pendente.

## 2. Textos selecionados e contextualizados corretamente — 2 pontos

**Entregue**: 2 textos (mínimo cumprido), contraste deliberado de registro
(técnico-científico vs. comunicação em saúde pública), proveniência completa
com licença verificada na fonte para os dois, justificativa das 3 técnicas
de NLP do enunciado com exemplo extraído do conteúdo real de cada texto
(não genérico), incluindo a observação explícita de que sentimento não se
aplica a nenhum dos dois (autocrítica já embutida na entrega, não escondida).

**Atualização**: a data de publicação/atualização do Texto 2 (Ministério da
Saúde) não foi localizada na página-fonte — não é mais um `TODO`, é nota de
proveniência definitiva (a página verificadamente não expõe esse campo; a
data de acesso registrada é a referência temporal disponível). Textos também
publicados no Google Drive, além de versionados no repositório. Critério
fechado.

## 3. Imagens entregues e bem justificadas em seu potencial para análise por IA — 2 pontos

**Entregue**: dataset fonte investigado a fundo antes de amostrar (contagem
real por categoria, extensões, checagem de duplicata por MD5 e por hash
perceptual com achado documentado de shortcut learning), 120 imagens
selecionadas e balanceadas com critério justificado, manifest completo com
aliases de duplicata, 12 amostras versionadas no repositório, justificativa
de Visão Computacional ligada ao formato real do dado (`dados-visuais.md`).

**Atualização**: as 120 imagens foram publicadas no Google Drive (link em
`README.md` e `assets/imagens/LEIA-ME.md`) — este era o maior risco da
entrega (a entrega física do principal artefato desta parte, não só um link
cosmético) e está resolvido. Critério fechado.

## 4. Documento resumo com explicações claras, objetivas e bem estruturadas — 2 pontos

**Entregue**: `document/ai_project_document_fiap.md` preenchido em todas as
seções do template FIAP (sem reescrever a estrutura), consolidando as três
partes e a governança em versão condensada, com links para os documentos
completos em vez de duplicar texto longo.

**Risco a monitorar, não necessariamente um problema**: a rubrica pede
explicações "claras, objetivas e bem estruturadas" dentro do documento
resumo — a estratégia adotada (condensar e linkar para `document/fase-01/*`
em vez de reproduzir tudo inline) é a leitura mais direta de "resumo", mas
depende de o avaliador efetivamente abrir os links. Se o critério for
avaliado só pelo que está literalmente dentro do arquivo `ai_project_
document_fiap.md`, sem seguir os links, o conteúdo ali é mais enxuto que o
material completo. **Risco: baixo-médio**, mitigável se o grupo quiser
expandir um pouco mais o texto condensado antes da entrega final (decisão
de escopo, não uma lacuna).

## 5. Cumprimento das orientações gerais e prazo de entrega — 1 ponto

**Entregue**: nenhum dado identificável de paciente, nenhum arquivo
volumoso commitado, proveniência registrada para as 4 bases, `TODO(humano)`
usado sempre que um dado não pôde ser verificado (nunca inventado).

**O que ainda não pode ser autoavaliado por mim**: (a) "testar os links em
janela anônima" — os 4 links já existem e foram publicados, mas confirmar
que abrem sem login é uma verificação que só o humano pode fazer (o agente
não tem como abrir navegador); (b) **prazo de entrega** — não tenho a
data-limite da atividade em nenhum documento deste repositório, então não
posso afirmar cumprimento de prazo; isso só o humano sabe. **Risco: baixo**,
dependente apenas de confirmação humana, não de trabalho pendente.

## Resumo do risco

| Critério | Pontos | Está pronto? |
|---|---|---|
| 1. Dataset numérico | 3 | Sim — link público publicado |
| 2. Textos | 2 | Sim — data do Texto 2 registrada como nota de proveniência, não mais TODO |
| 3. Imagens | 2 | Sim — link público publicado (era o maior risco da entrega) |
| 4. Documento resumo | 2 | Sim, com ressalva sobre profundidade inline vs. linkada |
| 5. Orientações e prazo | 1 | Regras de conduta cumpridas; falta só confirmação humana dos links em janela anônima e da data-limite |

**Ação restante antes da entrega**: o humano confirmar, em janela anônima,
que os 4 links do Google Drive abrem sem login — é a única verificação que
o agente não pode fazer sozinho.
