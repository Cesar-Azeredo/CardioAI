# Autoavaliação — Fase 2, contra a rubrica (seção 5bis.2 do AGENTS.md)

Autoavaliação crítica, critério por critério. Onde a nota provável não é
"cheia", digo por quê — o objetivo é identificar risco real antes da
correção, não validar o próprio trabalho. Redigida com apoio de assistente de
IA e revisada pelo grupo.

## 1. Relatos e mapa de conhecimento organizados — 2 pontos

**Entregue**:
- 10 frases de paciente em `assets/textos/fase-02/frases-sintomas-pacientes.txt`,
  cada uma com o que a pessoa sente, quando começou e como afeta a rotina;
  redação própria (maior sequência de palavras igual a uma página-fonte: 4),
  sem identificador; cada frase é um caso de teste com gabarito em
  `document/fase-02/gabarito-frases.md`.
- Mapa em `document/datasets/fase-02/mapa-conhecimento-sintomas.csv`, com as
  três colunas literais do enunciado (`Sintoma 1`, `Sintoma 2`,
  `Doença Associada`), 53 linhas e 26 conceitos. Todo Sintoma 1 é termo
  literal de página do Ministério da Saúde, com trecho-fonte conferido por
  script; variantes leigas marcadas como tal.
- Mapa e frases congelados por SHA-256.

**Risco**: o mapa cobre **3 doenças** (hipertensão, infarto, AVC). O
enunciado cita insuficiência cardíaca e angina como exemplo; ficaram de fora
por falta de fonte oficial equivalente — decisão de governança registrada em
`document/fase-02/governanca-e-vies.md`, mas um corretor que espere as cinco
doenças do exemplo pode descontar. A organização é densa (colunas de
proveniência, regras de inclusão); a ficha em
`document/datasets/fase-02/README.md` explica, mas é leitura longa.

## 2. Código de extração de informações funcional — 2 pontos

**Entregue**: `scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py` lê as
10 frases, extrai sintomas (RSLP, proximidade ordenada, negação estilo NegEx,
sobreposição, localização), sugere diagnóstico com nível de confiança e grava
`document/fase-02/resultado-extrator.md`. Protocolo pré-registrado e
congelado (`document/fase-02/protocolo-extrator.md`); 14 testes
pré-registrados + U15 passando; checagem de mutação 5/5; roda em venv limpa;
modo `--frase` para demonstração ao vivo.

**Risco**: o resultado é honesto e **modesto** — 9/10 contra 8/10 do casamento
exato, e empate 6/7 nas frases não contaminadas: a melhora vem só da frase
contaminada. A frase 7 conta como erro pelo critério pré-registrado. Um
corretor que leia só o placar pode achar pouco; a leitura correta (o método
não foi validado além do baseline) está no resultado e no README.

## 3. Dataset simples criado corretamente — 1 ponto

**Entregue**: `document/datasets/fase-02/frases-rotuladas-risco.csv` com o
cabeçalho literal `frase,situacao`, valores `alto risco` / `baixo risco`, 80
frases (40/40). Critério de rótulo ancorado em trechos literais das páginas
do Ministério da Saúde, registrado antes das frases
(`document/fase-02/criterio-rotulo-risco.md`); segurança do baixo risco,
quase-duplicata, vazamento, cláusula ND e gênero da voz conferidos por
`scripts/fase-02/06_verifica_dataset_risco.py`; conjunto-desafio de 18 frases
fora do treino; tudo congelado.

**Risco**: baixo para o ponto em si — o formato pedido está cumprido com
folga. A ressalva é de qualidade, e está documentada como resultado: o
dataset tem atalhos de palavra funcional ("mas" só no baixo risco, "eu" só no
alto) que a verificação não pegou, porque contava só palavras de conteúdo.

## 4. Classificador treinado e testado corretamente — 2 pontos

**Entregue**: `notebooks/fase-02/fase-02-tfidf-classificador-risco.ipynb`,
commitado **executado**. TF-IDF dentro de Pipeline (sem vazamento entre
treino e teste), regressão logística contra baseline, split fixo 75/25 com
matriz de confusão e relatório por classe, validação cruzada 5×10 com média e
desvio-padrão, recall de alto risco como métrica principal, falsos negativos
listados, coeficientes interpretados, desafio H1–H5 com teste contrafactual
de gênero e análises secundárias. Hipóteses pré-registradas
(`document/fase-02/protocolo-classificador.md`, commitado antes do notebook);
seção pós-hoc separada e marcada; na reexecução, as seções pré-registradas
saíram idênticas.

**Risco**: n = 80 — cada frase vale 5 pontos percentuais no split fixo, e a
validação cruzada mostra a oscilação (acurácia 0,812 ± 0,084). As
probabilidades não são calibradas (ficam entre 0,34 e 0,62 no desafio).
Tudo isso é declarado no notebook; o risco é o corretor ler "0,85" do split
sem ler a validação cruzada — o README põe os dois lado a lado.

## 5. Documentação clara e repositório público com README completo — 1 ponto

**Entregue**: bloco "Entrega 2" no `README.md`, em paralelo ao da Entrega 1,
com a tabela entregável → arquivo na ordem do enunciado, badge do Colab,
resumo dos resultados com os números reais, distorções encontradas e como
executar. Linha 0.2.0 no histórico. Repositório público — confirmado sem
autenticação (HTTP 200) em 2026-09-23.

**Risco**: a documentação é **extensa** (protocolos, critério, governança,
adendo). A tabela de entregáveis existe para o corretor achar cada item em
segundos, mas o volume pode pesar contra "clara". A seção "Descrição" do
template ainda fala só da Fase 1 — não foi alterada por ser seção do template
e do bloco da Entrega 1.

## 6. Vídeo de demonstração no YouTube (não listado) com link no GitHub — 2 pontos

**Pendente.** O vídeo ainda não foi gravado nem publicado, e o link não está
no README.

> ⚠️ TODO(humano): colar aqui e no `README.md` o link público do vídeo no YouTube (não listado)

**Risco**: **2 pontos em risco até o link entrar** — é o maior risco da
entrega, e é inteiramente trabalho humano. Sugestão de roteiro (até 4 min):
extrator ao vivo com `--frase` numa frase com negação e numa frase atípica;
notebook no Colab mostrando a matriz de confusão, a validação cruzada e o
falso negativo "…mas não dói nada". Testar o link em janela anônima.

## Resumo do risco

| Critério | Pontos | Está pronto? |
|---|---|---|
| 1. Relatos e mapa | 2 | Sim, com ressalva sobre cobrir 3 doenças, não 5 |
| 2. Código de extração | 2 | Sim — funcional e testado; resultado modesto, declarado |
| 3. Dataset | 1 | Sim |
| 4. Classificador | 2 | Sim — com n pequeno e probabilidades não calibradas declarados |
| 5. Documentação e repositório público | 1 | Sim — repositório público confirmado; documentação extensa |
| 6. Vídeo | 2 | **Não — pendente** |

**Ação restante**: gravar e publicar o vídeo e colar o link no `README.md` e
aqui. Itens "Ir Além" não foram feitos (não decididos). Só o humano pode
confirmar o prazo da atividade.
