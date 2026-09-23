# Adendo pós-execução — extrator de sintomas (Fase 2)

Registros feitos **depois** da execução única do extrator nas 10 frases
(2026-09-23). Nenhum deles altera regra do protocolo congelado
(`document/fase-02/protocolo-extrator.md`, que continua congelado), o mapa,
as frases ou o resultado de casamento.

## 1. U15 — teste adicionado após a execução única

**Por quê.** A checagem de mutação (`scripts/fase-02/05_checa_mutacao_testes.py`)
aplica em memória uma quebra de cada regra e verifica se algum teste falha.
Com a bateria pré-registrada U1–U14, uma mutação escapava: remover a regra
4.3 ("marcador de negação consumido por termo casado não é gatilho") não
derrubava nenhum teste. Motivo: em U1 ("sem fôlego") e U2 ("sem forças") o
`sem` é a **primeira** palavra do próprio termo, e a pré-negação só atinge
termos que começam **depois** do gatilho — então o `sem` não negaria o termo
nem com a regra removida. A regra 4.3 só faz diferença quando o `sem`
consumido poderia negar **outro** termo da mesma oração.

**O teste.** `scripts/fase-02/04_testa_extrator_adendo.py`, rotulado
"adicionado após a execução única":

| # | Entrada sintética | Esperado | Regra |
|---|---|---|---|
| U15 | "fiquei sem fôlego com tontura" | `sem fôlego` casado e não negado; `tontura` casada e **não** negada | 4.3 |

**O que ele muda.** Fecha uma lacuna de **cobertura** da bateria de testes.
Não altera regra, código de casamento nem resultado — o código já aplicava a
regra 4.3 corretamente (conferido antes, numa checagem avulsa). A bateria
pré-registrada U1–U14 continua como estava, no seu arquivo
(`scripts/fase-02/03_testa_extrator.py`, cujo SHA-256 está no cabeçalho do
resultado).

**Checagem de mutação depois do U15** (U1–U15):

| Mutação (em memória) | Testes que falham |
|---|---|
| janela = 1 (protocolo: 2) | U3, U9 |
| janela = 5 (protocolo: 2) | U7, U10 |
| `e` deixa de ser fronteira (4.2) | U5 |
| marcador consumido também vira gatilho (sem a regra 4.3) | **U15** — antes, nenhum |
| sem regra de localização (6) | U6, U8 |

5/5 mutações pegas.

## 2. Limitação de desenho: a oração restringe também o casamento

A segmentação por oração (protocolo 4.2) foi desenhada para limitar o
**escopo da negação**: vírgula, ponto, `mas`, `porém` e `e` encerram a
oração para que um "não" não negue sintoma de outra oração. Mas o mesmo
recorte também limita o **casamento** (protocolo 3.2: "sem cruzar fronteira
de oração"). Um termo cujas palavras ficam em orações diferentes não casa.

**Caso observado — frase 9:** "…estou com o braço fraco e formigando, só do
lado direito, …". O `e` separa "braço fraco" de "formigando", e a vírgula
separa "formigando" de "só do lado direito". Resultado: `formigando de um
lado` e `lado do corpo formigando` não casam; só `braço fraco` conta, e um
quadro característico de AVC (fraqueza + formigamento de um lado só) sai com
**confiança baixa** (1 conceito).

É **consequência do desenho, não bug**: o código faz o que o protocolo diz.
O custo é previsível para sintomas descritos em coordenação ("X e Y",
"X, Y") — justamente o jeito mais comum de um paciente enumerar sintomas.

**Próximo passo (não implementado):** segmentação separada para os dois
usos — orações para o escopo da negação e uma unidade maior (a frase inteira,
ou a sentença até o ponto) para o casamento. Qualquer mudança nesse sentido
exige novo protocolo pré-registrado e nova avaliação; não se aplica ao
resultado já registrado.

## 3. Explicações da divergência fora do arquivo gerado

**Por quê.** O extrator vai ser rodado ao vivo no vídeo. Até aqui, a coluna
"Explicação da divergência" de `document/fase-02/resultado-extrator.md` era
escrita à mão no arquivo gerado, e qualquer nova execução a apagaria.

**O que mudou.** Os textos aprovados pelo grupo foram movidos para
`document/fase-02/explicacoes-divergencia.md` (autoria humana, versionado).
O gerador passou a **mesclar** esse arquivo ao escrever o relatório. Só a
parte de escrita do relatório mudou (função `ler_explicacoes` e duas linhas
em `relatorio`); nenhuma regra de casamento, negação, pontuação ou confiança.

**Regressão.** Com o arquivo de explicações reproduzindo exatamente o texto
commitado, o resultado regenerado saiu **idêntico** ao commitado — tabela,
acertos, explicações e detalhe das 10 frases —, com duas únicas linhas
diferentes:

- **SHA-256 do código** no cabeçalho — muda porque o gerador mudou
  (`1cc1b79a…` → hash novo, registrado no cabeçalho a cada geração);
- **data da execução** no cabeçalho — toda regeneração é uma execução nova
  e registra quando aconteceu.

Os 14 testes pré-registrados e o U15 continuam passando.

**Correção de texto feita em seguida.** O parágrafo da nota abaixo da tabela
dizia que "uma nova execução do extrator regenera o arquivo e apaga esta
coluna" — deixou de ser verdade com a mesclagem. Esse parágrafo foi
reescrito em `explicacoes-divergencia.md` para descrever a mesclagem; a linha
de transparência ("Explicações redigidas com apoio de assistente de IA,
revisadas e aprovadas pelo grupo.") e os textos das frases 3, 7, 9 e 10 não
mudaram.

**Sobre reexecutar nas frases.** A regeneração acima reexecuta o extrator nas
10 frases, mas não é uma nova avaliação: o casamento é determinístico e a
saída de casamento saiu idêntica à da execução única, que continua sendo o
resultado registrado.
