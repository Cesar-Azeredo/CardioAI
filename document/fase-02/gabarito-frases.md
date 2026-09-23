# Gabarito das 10 frases — casos de teste do extrator

As 10 frases de `assets/textos/fase-02/frases-sintomas-pacientes.txt` são
**casos de teste**: cada uma sonda um comportamento específico do extrator de
sintomas. Esta tabela é o gabarito com que o extrator vai ser avaliado depois
de escrito. O número da frase é o número da linha no `.txt`.

## Regra: mapa e frases estão congelados

> **O mapa e as frases estão congelados. O mapa NÃO recebe variantes para
> acertar frases de teste. Adicionar 'fala ficou enrolada' ao mapa porque a
> frase 3 falhou é o mesmo overfitting que reescrever a frase — só que pela
> porta do mapa. Melhorias legítimas estão no MÉTODO de casamento, e só
> valem se decididas antes de rodar nas frases.**

**A partir de 2026-09-23, as 10 frases estão CONGELADAS e não mudam para
acomodar o extrator.** Casos de teste se escrevem independentes da
implementação. Se o extrator falhar numa frase escrita em linguagem natural,
isso é **resultado a reportar**, não motivo para reescrever a frase.

- O congelamento é imposto por máquina: `scripts/fase-02/01_verifica_mapa_e_frases.py`
  reprova se o SHA-256 de qualquer um dos dois arquivos mudar:
  - frases: `e124a24e4532e5f008fdfe0d47b6e5638c3cc53409350c39bf96bf731e48c91b`;
  - mapa: `79fae46c6cfd8418eaed30b39f8c84f8eca80b9f0e3ac086ceedac18b91d63c3`.
- **Último acréscimo antes do congelamento do mapa** — irradiação para o
  braço esquerdo (Sintoma 1 = `braço esquerdo`, literal na página de infarto,
  como LOCAL da irradiação da dor no peito; Sintoma 2 = `dor no braço
  esquerdo`, `dor que vai para o braço esquerdo`). Motivo: fonte e relevância
  clínica, **não** frase de teste. Conferido antes de acrescentar: a frase 1
  já tinha 3 termos literais de Infarto (dor no peito, suor frio, falta de
  ar) contra 1 variante de Hipertensão (dor no peito). Depois do acréscimo, a
  frase 1 ganha 1 termo (`braço esquerdo`, pelo Sintoma 1 literal; as duas
  variantes novas não casam, porque a frase diz "dor no peito forte que vai
  para o braço esquerdo"). Nenhuma outra frase mudou. `dor na barriga`
  continua fora: "abdome" não forma termo contínuo de sintoma na página.
- O mesmo vale para este gabarito: o diagnóstico esperado de cada frase não
  muda depois que o extrator existir.
- **Histórico registrado**: antes do congelamento, a frase 3 chegou a ser
  reescrita ("minha fala ficou enrolada" → "estou com a fala enrolada")
  porque o casamento literal não reconhecia a primeira forma. A mudança foi
  **revertida** na revisão do grupo, pelo motivo acima: seria ajustar o
  conjunto de teste ao modelo. A frase 3 está na redação original.
- Mudar uma frase depois disto exige decisão explícita do grupo, registrada
  aqui com o motivo, e novo hash no verificador.

## O que o extrator precisa reportar

Para cada frase: a doença sugerida, **quantos sintomas casou** (e quais) e um
**nível de confiança**. Acertar com um único sintoma é resultado honesto
desde que venha rotulado como tal ("Infarto, baixa confiança (1 sintoma)").
**Não** se adota número mínimo de sintomas para forçar ou evitar falha.

## Gabarito

- **Diagnóstico esperado** é o que o mapa de conhecimento sustenta para
  aquela frase — não é diagnóstico clínico. Projeto acadêmico; nada aqui
  serve para decisão médica.
- **Termos do mapa presentes** saiu da saída do verificador (casamento
  literal, palavra inteira, sem diferenciar maiúscula). **Não é o extrator**:
  é o que um casamento ingênuo encontra — a linha de base que o extrator
  precisa superar (negação, sobreposição, desempate).

| # | Comportamento que a frase sonda | Diagnóstico esperado | Termos do mapa presentes (casamento literal) |
|---|---|---|---|
| 1 | **Caso claro de infarto**, com termos literais da fonte e mais de um sintoma | **Infarto** | braço esquerdo, dor no peito, suor frio, falta de ar (literais de Infarto); dor no peito também é variante de Hipertensão |
| 2 | **Caso claro de infarto**, misturando termo literal, variante leiga e flexão (`pálido`) | **Infarto** | sensação de desmaio (literal); aperto no peito, pálido (variantes) — todos Infarto |
| 3 | **Caso claro de AVC** em linguagem natural: `minha fala ficou enrolada` e `formigamento no lado esquerdo do corpo` não têm a forma de nenhum termo do mapa; só `fraqueza` casa, e ela é compartilhada | **AVC** | fraqueza (AVC e Hipertensão) — só um termo, e ambíguo |
| 4 | **Caso claro de AVC** com **sobreposição de termos**: `dor de cabeça súbita` (AVC) contém `dor de cabeça` (Hipertensão) — o extrator precisa preferir o termo mais longo | **AVC** | dor de cabeça súbita, confusão mental (AVC); dor de cabeça (Hipertensão); perdendo o equilíbrio (variante AVC) |
| 5 | **Caso claro de hipertensão** com termo exclusivo (`zumbido no ouvido`), variante leiga e um termo compartilhado | **Hipertensão** | dor de cabeça, zumbido no ouvido (literais); sangue pelo nariz (variante) — todos Hipertensão |
| 6 | **Caso claro de hipertensão** só com termos exclusivos da fonte | **Hipertensão** | visão embaçada, sangramento nasal (Hipertensão) |
| 7 | **Sintoma compartilhado — desempate**: `tontura` e `dor de cabeça` existem em Hipertensão e em AVC; sem início súbito nem lateralidade, nada na frase separa as duas | **Ambíguo: Hipertensão ou AVC** — o esperado é o extrator **explicitar a ambiguidade**, não escolher em silêncio | tontura (literal AVC, variante Hipertensão); dor de cabeça (Hipertensão) |
| 8 | **Só variante leiga**, nenhum termo literal da fonte (confirmado pelo verificador: zero termos literais na frase) | **Infarto** | peso no peito, sem fôlego, suando frio (variantes Infarto) |
| 9 | **Negação explícita**: `Não sinto dor no peito` — um casamento ingênuo conta `dor no peito` para Infarto e Hipertensão e empata com AVC | **AVC** (dor no peito negada não pode contar) | dor no peito (literal Infarto; variante Hipertensão) — **negado**; braço fraco (variante AVC) |
| 10 | **Infarto atípico**: pessoa diabética, falta de ar e mal-estar, **sem dor no peito**. A página do Ministério afirma que nesse perfil o infarto pode ocorrer sem sinais específicos | **Infarto, baixa confiança (1 sintoma)** | falta de ar (Infarto) — só um termo |

## Notas sobre os casos que devem expor limitação

**Frase 3 (linguagem natural).** A frase descreve um AVC típico, mas do jeito
que uma pessoa fala. O casamento literal só encontra `fraqueza`, que o mapa
associa a AVC e a Hipertensão. Se o extrator devolver ambíguo ou errado aqui,
isso é o resultado a reportar: mostra o limite de um extrator baseado em
lista de termos diante de variação natural de linguagem ("minha fala ficou
enrolada" ≠ "fala enrolada"). A frase **não** será reescrita para passar.

**Frase 7 (desempate).** Uma contagem simples de termos daria Hipertensão 2
× AVC 1 (`tontura` conta para as duas, `dor de cabeça` só casa inteira com
Hipertensão, porque o termo de AVC é o mais longo `dor de cabeça súbita`).
Isso **não** é evidência de hipertensão — é efeito do tamanho do termo. Um
extrator que responde "Hipertensão" aqui sem sinalizar a ambiguidade está
errando com confiança.

**Frase 10 (infarto atípico).** O esperado é **Infarto com baixa confiança
(1 sintoma)**. `falta de ar` só aparece em Infarto no mapa, então o extrator
provavelmente acerta a doença — por um único termo, e isso tem que vir dito
na saída. O que ele não captura:

- `mal-estar` não casa com `mal-estar súbito`, e o mapa não tem `mal-estar`
  sozinho como variante — sem o "súbito" o termo perde o sentido de alerta
  que tem na fonte;
- `diabética` é o fator de perfil que, segundo a fonte, torna a apresentação
  atípica — e o mapa é de sintoma → doença, não de perfil;
- `sem dor nenhuma` é negação de dor sem nomear o local.

**A falha perigosa deste perfil não é demonstrada aqui, e sim na Parte 2**,
no classificador de risco. A hipótese a testar lá: uma frase sem "dor" tende
a ser classificada como **baixo risco**, mesmo sendo um possível infarto em
curso — o falso negativo caro que a assimetria de custo da Fase 1 descreve.
Se a hipótese se confirmar, essa é a demonstração para o vídeo; se não, o
resultado real é o que se reporta.
