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

**O que falta para fechar o critério**: o **link público externo** (Drive/
OneDrive) do dataset ainda não existe — está marcado `TODO(humano)` no
`README.md`. O enunciado pede esse link explicitamente na Parte 1, mesmo o
CSV já estando versionado no GitHub. Sem ele, o critério não está 100%
cumprido, apesar de todo o resto (organização, explicação, script) estar
pronto. **Risco: baixo-médio** — é só publicar e colar o link, mas até isso
acontecer o item está objetivamente incompleto.

## 2. Textos selecionados e contextualizados corretamente — 2 pontos

**Entregue**: 2 textos (mínimo cumprido), contraste deliberado de registro
(técnico-científico vs. comunicação em saúde pública), proveniência completa
com licença verificada na fonte para os dois, justificativa das 3 técnicas
de NLP do enunciado com exemplo extraído do conteúdo real de cada texto
(não genérico), incluindo a observação explícita de que sentimento não se
aplica a nenhum dos dois (autocrítica já embutida na entrega, não escondida).

**O que falta para fechar o critério**: a data de publicação/atualização do
Texto 2 (Ministério da Saúde) não foi localizada na página-fonte — marcado
`TODO(humano)`, com sugestão de verificar via Wayback Machine se a rubrica
exigir essa data especificamente. Não há requisito explícito de link externo
para os textos (o enunciado pede "armazenar em subpasta do repositório", já
cumprido), então este critério está **objetivamente mais perto de completo**
que os critérios 1 e 3. **Risco: baixo.**

## 3. Imagens entregues e bem justificadas em seu potencial para análise por IA — 2 pontos

**Entregue**: dataset fonte investigado a fundo antes de amostrar (contagem
real por categoria, extensões, checagem de duplicata por MD5 e por hash
perceptual com achado documentado de shortcut learning), 120 imagens
selecionadas e balanceadas com critério justificado, manifest completo com
aliases de duplicata, 12 amostras versionadas no repositório, justificativa
de Visão Computacional ligada ao formato real do dado (`dados-visuais.md`).

**O que falta para fechar o critério — este é o maior risco da entrega**: as
120 imagens em resolução completa **existem só localmente**
(`/Users/cesar/Downloads/cardioia-fase1-imagens-selecionadas/`, fora do
repositório) e **ainda não foram publicadas em nenhum lugar acessível ao
corretor**. O enunciado exige "imagens entregues" e link público — hoje, o
corretor só consegue ver as 12 amostras reduzidas no GitHub. Enquanto o link
não for publicado, este critério está de fato **incompleto**, não só
faltando um link cosmético como no critério 1 — é a entrega física do
principal artefato desta parte que ainda não aconteceu. **Risco: alto até o
upload acontecer.**

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

**O que falta / não pode ser autoavaliado por mim**: (a) "testar os links em
janela anônima" — não é possível ainda, os links não existem; (b) **prazo
de entrega** — não tenho a data-limite da atividade em nenhum documento
deste repositório, então não posso afirmar cumprimento de prazo; isso só o
humano sabe. **Risco: médio**, inteiramente dependente de ação humana
(publicar os 2-3 links pendentes e confirmar a data-limite), não de
qualidade do trabalho já feito.

## Resumo do risco

| Critério | Pontos | Está pronto? |
|---|---|---|
| 1. Dataset numérico | 3 | Conteúdo sim; link público **não** |
| 2. Textos | 2 | Sim, com 1 TODO menor (data do Texto 2) |
| 3. Imagens | 2 | Conteúdo sim; **upload/link público não existe ainda — maior risco da entrega** |
| 4. Documento resumo | 2 | Sim, com ressalva sobre profundidade inline vs. linkada |
| 5. Orientações e prazo | 1 | Regras de conduta cumpridas; link e prazo dependem do humano |

**Ação de maior prioridade antes da entrega**: publicar o link das 120
imagens (critério de maior risco) e do dataset numérico, colar os dois no
`README.md`, testar ambos em janela anônima, e então remover os `TODO(humano)`
correspondentes.
