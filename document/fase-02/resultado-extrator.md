# Resultado do extrator de sintomas — Fase 2

> **Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.**

Arquivo **gerado** por `scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py` seguindo `document/fase-02/protocolo-extrator.md`. Não editar à mão.

## Cabeçalho da execução

- Data: 2026-09-23T11:45:06-03:00
- Protocolo `document/fase-02/protocolo-extrator.md`: `90ed4cf356de81d400f25dd3b2f2cc303b01d9cb3bac67880b1a7a4aeaea2da4`
- Mapa `document/datasets/fase-02/mapa-conhecimento-sintomas.csv`: `79fae46c6cfd8418eaed30b39f8c84f8eca80b9f0e3ac086ceedac18b91d63c3`
- Frases `assets/textos/fase-02/frases-sintomas-pacientes.txt`: `e124a24e4532e5f008fdfe0d47b6e5638c3cc53409350c39bf96bf731e48c91b`
- Código `scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py`: `589165b6a71599d052da9e8aec9780d9e57b07050e180e65678c4f910b649657`
- Testes `scripts/fase-02/03_testa_extrator.py`: `4731e09094a3b645400363f70747cc3e0a23f889d94247562e81b55d9addd9cb`
- Python 3.12.14, nltk 3.9.1
- Recursos da NLTK (protocolo 2.5):
  - `rslp`: confere — esperado `f482f9666a2a76cdd4acab16b01a44b002550ebaac29906dbd5a1bbc281e4f8b`, encontrado `f482f9666a2a76cdd4acab16b01a44b002550ebaac29906dbd5a1bbc281e4f8b`
  - `stopwords`: confere — esperado `48c0e52d8b52546e827f53761fb30300c0ab94f70660d28bd65ba0a86270946b`, encontrado `48c0e52d8b52546e827f53761fb30300c0ab94f70660d28bd65ba0a86270946b`

## Avaliação (protocolo 10.4)

| # | Gabarito | Baseline exato | Método | Acerto baseline | Acerto método | Contaminada | Explicação da divergência |
|---|---|---|---|---|---|---|---|
| 1 | Infarto | Infarto (alta) | Infarto (alta) | acerto | acerto | sim | — |
| 2 | Infarto | Infarto (alta) | Infarto (alta) | acerto | acerto | não | — |
| 3 | AVC | ambíguo:AVC+Hipertensão (ambíguo) | AVC (alta) | erro | acerto | sim | O casamento exato só encontrou "fraqueza", compartilhada entre AVC e hipertensão, e empatou. O método casou "fala ficou enrolada" e "formigamento no lado esquerdo do corpo" pela janela de proximidade. A frase é contaminada: já sabíamos que ela falhava, então o acerto não prova que a janela generaliza. |
| 4 | AVC | AVC (alta) | AVC (alta) | acerto | acerto | não | — |
| 5 | Hipertensão | Hipertensão (alta) | Hipertensão (alta) | acerto | acerto | não | — |
| 6 | Hipertensão | Hipertensão (média) | Hipertensão (média) | acerto | acerto | não | — |
| 7 | ambíguo:AVC+Hipertensão | Hipertensão (média) | Hipertensão (média) | erro | erro | não | Os dois métodos deram hipertensão, e o gabarito esperava ambíguo. O AVC não pontua em "dor de cabeça" porque o termo do Ministério é "dor de cabeça súbita" — a característica que distingue clinicamente a cefaleia do AVC. Conta como erro pelo critério pré-registrado, mas o resultado do sistema é clinicamente defensável, e o gabarito pode ter sido o julgamento mais fraco. |
| 8 | Infarto | Infarto (alta) | Infarto (alta) | acerto | acerto | não | — |
| 9 | AVC | AVC (baixa) | AVC (baixa) | acerto | acerto | não | A negação funcionou — "dor no peito" saiu negada. Mas "formigando" não casou porque o casamento respeita a oração, e AVC saiu com confiança baixa. Limitação de desenho documentada. |
| 10 | Infarto, confiança baixa | Infarto (baixa) | Infarto (baixa) | doença acerto; confiança acerto | doença acerto; confiança acerto | sim | Infarto com baixa confiança e 1 sintoma, como esperado. É o perfil em que o Ministério alerta que o infarto pode ocorrer sem sinais específicos. |

Explicações redigidas com apoio de assistente de IA, revisadas e aprovadas pelo grupo.

> A coluna "Explicação da divergência" foi escrita pelo grupo **depois** da execução única, como prevê o protocolo (10.4) (revisão de Cesar Martinho de Azeredo). O texto vive em `document/fase-02/explicacoes-divergencia.md` (autoria humana) e é mesclado pelo gerador a cada regeneração; o restante deste arquivo é saída do extrator.

Acerto de doença — baseline exato: **8/10**; método: **9/10**.
Só nas frases não contaminadas (2, 4, 5, 6, 7, 8, 9) — baseline: **6/7**; método: **6/7**.

Frases contaminadas (protocolo 10.3) — acerto do método nelas não conta como evidência a favor da decisão:

- Frase 1: regra de localização (6) — a frase cita braço esquerdo ao lado de dor no peito
- Frase 3: janela de 2 tokens (3.2) — o casamento exato falha em "minha fala ficou enrolada"
- Frase 10: nível "baixa" = 1 conceito (8) — a frase tem um único termo casado literalmente

## Detalhe por frase (protocolo 9)

### Frase 1

> Desde hoje cedo estou com uma dor no peito forte que vai para o braço esquerdo, com suor frio e falta de ar, e não consegui nem sair da cama para ir trabalhar.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `braço esquerdo` ← termo 'braço esquerdo' — Infarto (linha 20, 21)
  - `dor peito` ← termo 'dor no peito' / 'dores no peito' — Hipertensão (linha 2, 3); Infarto (linha 17, 18)
  - `suor frio` ← termo 'suando frio' / 'suor frio' — Infarto (linha 26, 27)
  - `falta ar` ← termo 'falta de ar' / 'faltando o ar' — Infarto (linha 29, 30, 31)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Infarto 4 (braço esquerdo, desconforto na região peitoral / dor no peito, falta de ar, suor frio); Hipertensão 1 (dores no peito)
- **Sugestão: Infarto — confiança alta**

**Baseline exato:**

- Termos casados:
  - `dor no peito` ← termo 'dor no peito' — Hipertensão (linha 2); Infarto (linha 17, 18)
  - `braço esquerdo` ← termo 'braço esquerdo' — Infarto (linha 20, 21)
  - `suor frio` ← termo 'suor frio' — Infarto (linha 26, 27)
  - `falta de ar` ← termo 'falta de ar' — Infarto (linha 29, 30, 31)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Infarto 4 (braço esquerdo, desconforto na região peitoral / dor no peito, falta de ar, suor frio); Hipertensão 1 (dores no peito)
- **Sugestão: Infarto — confiança alta**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

### Frase 2

> Há umas duas horas me deu um aperto no peito enquanto eu subia a escada do prédio, fiquei pálido e com sensação de desmaio, e tive que sentar no degrau porque não conseguia continuar.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `aperto peito` ← termo 'aperto no peito' — Infarto (linha 23)
  - `pálido` ← termo 'pálido' — Infarto (linha 28)
  - `sensação desmaio` ← termo 'sensação de desmaio' — Infarto (linha 32, 33)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Infarto 3 (aperto sobre o tórax / sensação de peso, palidez, sensação de desmaio)
- **Sugestão: Infarto — confiança alta**

**Baseline exato:**

- Termos casados:
  - `aperto no peito` ← termo 'aperto no peito' — Infarto (linha 23)
  - `pálido` ← termo 'pálido' — Infarto (linha 28)
  - `sensação de desmaio` ← termo 'sensação de desmaio' — Infarto (linha 32, 33)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Infarto 3 (aperto sobre o tórax / sensação de peso, palidez, sensação de desmaio)
- **Sugestão: Infarto — confiança alta**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

### Frase 3

> Desde a hora do almoço sinto fraqueza e formigamento no lado esquerdo do corpo, minha fala ficou enrolada e o garfo caiu da minha mão porque não consegui segurar.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `fraqueza` ← termo 'fraqueza' — AVC (linha 51, 52); Hipertensão (linha 11, 12)
  - `formigamento lado corpo` ← termo 'formigamento em um lado do corpo' — AVC (linha 53, 54)
  - `fala enrolada` ← termo 'fala enrolada' — AVC (linha 38)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): AVC 3 (alteração da fala ou compreensão, formigamento em um lado do corpo, fraqueza); Hipertensão 1 (fraqueza)
- **Sugestão: AVC — confiança alta**

**Baseline exato:**

- Termos casados:
  - `fraqueza` ← termo 'fraqueza' — AVC (linha 51, 52); Hipertensão (linha 11, 12)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): AVC 1 (fraqueza); Hipertensão 1 (fraqueza)
- **Sugestão: AVC, Hipertensão — confiança ambíguo**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

### Frase 4

> Faz mais ou menos uma hora que veio uma dor de cabeça súbita, muito forte, fiquei com confusão mental e perdendo o equilíbrio, e precisei largar a louça pela metade.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `dor cabeça súbita` ← termo 'dor de cabeça súbita' — AVC (linha 43, 44)
  - `confusão mental` ← termo 'confusão mental' — AVC (linha 36, 37)
  - `perdendo equilíbrio` ← termo 'perdendo o equilíbrio' — AVC (linha 45)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): AVC 3 (alteração do equilíbrio, confusão mental, dor de cabeça súbita)
- **Sugestão: AVC — confiança alta**

**Baseline exato:**

- Termos casados:
  - `dor de cabeça súbita` ← termo 'dor de cabeça súbita' — AVC (linha 43, 44)
  - `confusão mental` ← termo 'confusão mental' — AVC (linha 36, 37)
  - `perdendo o equilíbrio` ← termo 'perdendo o equilíbrio' — AVC (linha 45)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): AVC 3 (alteração do equilíbrio, confusão mental, dor de cabeça súbita)
- **Sugestão: AVC — confiança alta**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

### Frase 5

> Há três dias tenho dor de cabeça e zumbido no ouvido quase todo fim de tarde, ontem saiu sangue pelo nariz, e estou evitando dirigir até o trabalho.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `dor cabeça` ← termo 'dor de cabeça' / 'dor na cabeça' — Hipertensão (linha 4, 5)
  - `zumbido ouvido` ← termo 'zumbido no ouvido' — Hipertensão (linha 9, 10)
  - `sangue nariz` ← termo 'sangue pelo nariz' — Hipertensão (linha 15)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Hipertensão 3 (dor de cabeça, sangramento nasal, zumbido no ouvido)
- **Sugestão: Hipertensão — confiança alta**

**Baseline exato:**

- Termos casados:
  - `dor de cabeça` ← termo 'dor de cabeça' — Hipertensão (linha 4, 5)
  - `zumbido no ouvido` ← termo 'zumbido no ouvido' — Hipertensão (linha 9, 10)
  - `sangue pelo nariz` ← termo 'sangue pelo nariz' — Hipertensão (linha 15)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Hipertensão 3 (dor de cabeça, sangramento nasal, zumbido no ouvido)
- **Sugestão: Hipertensão — confiança alta**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

### Frase 6

> Desde a semana passada estou com visão embaçada e tive sangramento nasal duas vezes, parei de ler à noite e fico com receio de sair de casa sozinha.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `visão embaçada` ← termo 'visão embaçada' — Hipertensão (linha 13, 14)
  - `sangramento nasal` ← termo 'sangramento nasal' — Hipertensão (linha 15, 16)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Hipertensão 2 (sangramento nasal, visão embaçada)
- **Sugestão: Hipertensão — confiança média**

**Baseline exato:**

- Termos casados:
  - `visão embaçada` ← termo 'visão embaçada' — Hipertensão (linha 13, 14)
  - `sangramento nasal` ← termo 'sangramento nasal' — Hipertensão (linha 15, 16)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Hipertensão 2 (sangramento nasal, visão embaçada)
- **Sugestão: Hipertensão — confiança média**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

### Frase 7

> Desde ontem sinto tontura e dor de cabeça, e hoje passei o dia deitado em vez de cuidar da horta como sempre faço.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `tontura` ← termo 'tonto' / 'tontura' / 'tonturas' — AVC (linha 47, 48); Hipertensão (linha 6, 7, 8)
  - `dor cabeça` ← termo 'dor de cabeça' / 'dor na cabeça' — Hipertensão (linha 4, 5)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Hipertensão 2 (dor de cabeça, tonturas); AVC 1 (tontura)
- **Sugestão: Hipertensão — confiança média**

**Baseline exato:**

- Termos casados:
  - `tontura` ← termo 'tontura' — AVC (linha 47, 48); Hipertensão (linha 6)
  - `dor de cabeça` ← termo 'dor de cabeça' — Hipertensão (linha 4, 5)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Hipertensão 2 (dor de cabeça, tonturas); AVC 1 (tontura)
- **Sugestão: Hipertensão — confiança média**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

### Frase 8

> Faz uns dez minutos que estou com um peso no peito e sem fôlego, fiquei suando frio dentro do ônibus e tive que descer antes do meu ponto.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `peso peito` ← termo 'peso no peito' — Infarto (linha 25)
  - `sem fôlego` ← termo 'sem fôlego' — Infarto (linha 29)
  - `suando frio` ← termo 'suando frio' / 'suor frio' — Infarto (linha 26, 27)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Infarto 3 (aperto sobre o tórax / sensação de peso, falta de ar, suor frio)
- **Sugestão: Infarto — confiança alta**

**Baseline exato:**

- Termos casados:
  - `peso no peito` ← termo 'peso no peito' — Infarto (linha 25)
  - `sem fôlego` ← termo 'sem fôlego' — Infarto (linha 29)
  - `suando frio` ← termo 'suando frio' — Infarto (linha 26)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Infarto 3 (aperto sobre o tórax / sensação de peso, falta de ar, suor frio)
- **Sugestão: Infarto — confiança alta**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

### Frase 9

> Não sinto dor no peito, mas desde hoje de manhã estou com o braço fraco e formigando, só do lado direito, e não consegui abotoar a camisa para sair.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `braço fraco` ← termo 'braço fraco' — AVC (linha 51)
- Termos negados:
  - `dor peito` ← termo 'dor no peito' / 'dores no peito' — Hipertensão (linha 2, 3); Infarto (linha 17, 18) — gatilho `nao`
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): AVC 1 (fraqueza)
- **Sugestão: AVC — confiança baixa**

**Baseline exato:**

- Termos casados:
  - `braço fraco` ← termo 'braço fraco' — AVC (linha 51)
- Termos negados:
  - `dor no peito` ← termo 'dor no peito' — Hipertensão (linha 2); Infarto (linha 17, 18) — gatilho `nao`
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): AVC 1 (fraqueza)
- **Sugestão: AVC — confiança baixa**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

### Frase 10

> Sou diabética e desde ontem à noite sinto falta de ar e um mal-estar que não passa, sem dor nenhuma, e hoje não tive forças nem para fazer o almoço.

**Método (RSLP + proximidade ordenada):**

- Termos casados:
  - `falta ar` ← termo 'falta de ar' / 'faltando o ar' — Infarto (linha 29, 30, 31)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Infarto 1 (falta de ar)
- **Sugestão: Infarto — confiança baixa**

**Baseline exato:**

- Termos casados:
  - `falta de ar` ← termo 'falta de ar' — Infarto (linha 29, 30, 31)
- Termos negados: —
- Localização descartada (sem dor na oração): —
- Pontuação (conceitos distintos): Infarto 1 (falta de ar)
- **Sugestão: Infarto — confiança baixa**

*Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica.*

