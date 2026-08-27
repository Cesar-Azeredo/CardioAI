# Dados textuais — Parte 2 (NLP)

Dois textos, escolhidos de propósito por contraste de registro — um técnico-
científico, outro de comunicação em saúde pública. Ficha completa de
proveniência (autor, licença, contagem real de palavras/caracteres,
processamento aplicado) em `assets/textos/PROVENIENCIA.md`. Extração
reprodutível em `scripts/fase-01/04_prepara_textos.py`.

- **Texto 1**: Pellanda, L. C. (2014). *Trajetórias da Saúde Cardiovascular:
  Epidemiologia do Curso da Vida no Brasil* [editorial]. Arquivos Brasileiros
  de Cardiologia, 102(5), 418–419. DOI 10.5935/abc.20140065. CC BY-NC 3.0.
  1.608 palavras, 10.790 caracteres.
- **Texto 2**: Ministério da Saúde. *Hipertensão (pressão alta)*. Saúde de A a
  Z. CC BY-ND 3.0 (Sem Derivações — salvo **sem nenhuma alteração de
  conteúdo**, só extração e normalização de espaço em branco). 858 palavras,
  5.547 caracteres.

## O contraste de registro

Os dois textos falam do mesmo domínio (risco cardiovascular) em dois
vocabulários que quase não se sobrepõem. O Texto 1 é escrito por uma
cardiologista para outros médicos e pesquisadores: usa termos como
"aterosclerose", "síndrome metabólica", "programação intrauterina das
doenças crônicas", cita 23 referências numeradas e discute "curva em U" de
risco em função do peso ao nascer. O Texto 2 é escrito pelo Ministério da
Saúde para qualquer cidadão: mesmo assunto (risco cardiovascular), mas
traduzido — o exemplo mais direto desse contraste é como o texto expressa o
valor de corte diagnóstico: "os valores das pressões máxima e mínima são
iguais ou ultrapassam os 140/90 mmHg **(ou 14 por 9)**". O "(ou 14 por 9)" é
exatamente o trabalho que o chatbot da Fase 5 vai ter que fazer
automaticamente: pegar uma grandeza clínica e devolver a forma como um
paciente brasileiro realmente fala. Esse par de textos é, então, não só
corpus de treino, mas **um exemplo já pronto do problema de tradução
clínico→leigo** que a Fase 5 precisa resolver — o baseline de como isso é
feito por humanos.

## As três técnicas de NLP do enunciado

### 1. Extração de sintomas

O Texto 2 tem uma seção `Sintomas` dedicada e já delimitada: *"Os sintomas da
hipertensão costumam aparecer somente quando a pressão sobe muito: podem
ocorrer dores no peito, dor de cabeça, tonturas, zumbido no ouvido, fraqueza,
visão embaçada e sangramento nasal."* Isso é, literalmente, uma lista de
entidades de sintoma separadas por vírgula, com um cabeçalho de seção que já
funciona como rótulo — um extrator baseado em regras (lista de termos) ou um
NER treinado teria aqui um vocabulário-semente pronto (7 sintomas nomeados em
linguagem de paciente) para reconhecer as mesmas entidades quando aparecerem
com outra formulação em uma mensagem de chat (ex.: "minha visão ficou
embaçada" → mapeado à mesma entidade "visão embaçada").

O Texto 1 **não tem lista de sintomas de paciente** — ele descreve fatores de
risco e desfechos em nível populacional/estatístico ("recém-nascidos com peso
de nascimento inferior a 2.500 g apresentaram maior incidência de doença
cardiovascular"), não sintomas relatados por um indivíduo. Esse contraste é
em si informativo: extração de sintomas funciona sobre texto de paciente ou
de orientação ao paciente (Texto 2), não sobre um editorial epidemiológico
(Texto 1).

**Uso concreto na Fase 5**: o vocabulário de sintomas do Texto 2 vira a lista
de entidades-alvo que o chatbot precisa reconhecer no relato livre do
paciente, para então orientar (buscar atendimento, medir a pressão, etc.)
usando a mesma lógica que o próprio Ministério da Saúde documenta.

### 2. Classificação de tópicos

O Texto 2 já vem estruturado com cabeçalhos que **são**, na prática, rótulos
de tópico: `Causas`, `Sintomas`, `Diagnóstico`, `Tratamento`, `Prevenção`,
`Profissionais de saúde`. Isso não é uma interpretação nossa — é a própria
organização da página. Um classificador de tópicos supervisionado poderia
usar exatamente esses parágrafos com seus cabeçalhos como pares
(texto, rótulo) de treino, e essa mesma taxonomia (causa / sintoma /
diagnóstico / tratamento / prevenção) generaliza para qualquer outra doença
do "Saúde de A a Z" — é um esqueleto de intenção reaproveitável.

O Texto 1 é tematicamente mais denso e não vem pré-rotulado: dentro de um
único editorial, aparecem subtemas técnicos distintos — peso ao nascer como
marcador de risco, síndrome metabólica na adolescência, expressão gênica
miocárdica, interação gene-ambiente. Um modelo de tópicos não supervisionado
(ex.: agrupar por similaridade de vocabulário) encontraria esses subtemas
dentro do próprio texto científico, em contraste com a taxonomia já pronta e
explícita do Texto 2.

**Uso concreto na Fase 5**: a taxonomia extraída do Texto 2
(causa/sintoma/diagnóstico/tratamento/prevenção) é candidata direta ao
roteamento de intenção do chatbot — decidir se a pergunta do paciente é
"por que isso acontece", "o que eu sinto", "como eu confirmo" ou "o que eu
faço".

### 3. Análise de sentimento

Nenhum dos dois textos deste corpus é relato de paciente — o Texto 1 é
prosa científica formal e neutra ("A adoção de um modelo de curso de vida
tem, portanto, o potencial de alterar significativamente o paradigma de
prevenção..."), e o Texto 2 é prosa institucional informativa, também neutra
("A hipertensão arterial ou pressão alta é uma doença crônica caracterizada
pelos níveis elevados da pressão sanguínea nas artérias."). **Análise de
sentimento pressupõe texto que carregue uma opinião, queixa ou estado
emocional de quem fala — isto é, relato de paciente, mensagem de chat,
avaliação —, não um editorial revisado por pares nem uma página
institucional.** Aplicar um classificador de sentimento a qualquer um destes
dois textos não geraria sinal útil: os dois foram escritos para informar, não
para expressar emoção.

**Por isso, este corpus não serve para treinar ou validar sentimento — serve
de baseline de vocabulário e de registro.** Ele documenta como o vocabulário
técnico (Texto 1) e o vocabulário leigo-institucional (Texto 2) descrevem o
mesmo domínio clínico em tom neutro. Quando a Fase 5 coletar relatos reais de
pacientes (que aí sim carregam sentimento — ansiedade, alívio, frustração com
o tratamento), esse baseline serve de referência de contraste: permite
diferenciar o que é "vocabulário neutro do domínio" do que é efetivamente
"carga emocional do paciente" no texto novo.

## Referência formal e proveniência

Detalhes completos — autor, afiliação, DOI, ISSN, licença exata, contagem
real de palavras e caracteres, e o processamento aplicado a cada texto —
estão em `assets/textos/PROVENIENCIA.md`, gerado automaticamente por
`scripts/fase-01/04_prepara_textos.py` a partir das próprias páginas-fonte
(nenhum metadado completado de memória).

## Como reproduzir

```bash
python scripts/fase-01/04_prepara_textos.py
```

Baixa as duas páginas-fonte, extrai o texto do corpo (descartando
menu/rodapé/links relacionados), salva os dois `.txt` em `assets/textos/` e
regrava `assets/textos/PROVENIENCIA.md` com as contagens reais.
