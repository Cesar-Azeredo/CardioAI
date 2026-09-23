# Explicações da divergência — resultado do extrator (Fase 2)

Arquivo de **autoria humana**, versionado. O gerador
(`scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py`) lê este arquivo e
**mescla** cada texto na coluna "Explicação da divergência" de
`document/fase-02/resultado-extrator.md`, e a seção "Nota abaixo da tabela"
logo abaixo da tabela. Regenerar o resultado (por exemplo, rodando o extrator
ao vivo no vídeo) não apaga nada daqui. Frase sem seção aqui sai com "—".

Formato lido pelo gerador: cada seção começa com `## Frase N` ou
`## Nota abaixo da tabela`; o texto da seção vai até a próxima seção. O texto
de uma frase vira uma única célula da tabela (quebras de linha viram espaço).

Textos revisados e aprovados pelo grupo (revisão de Cesar Martinho de
Azeredo), redigidos com apoio de assistente de IA.

## Nota abaixo da tabela

Explicações redigidas com apoio de assistente de IA, revisadas e aprovadas pelo grupo.

> A coluna "Explicação da divergência" foi escrita pelo grupo **depois** da execução única, como prevê o protocolo (10.4) (revisão de Cesar Martinho de Azeredo). O texto vive em `document/fase-02/explicacoes-divergencia.md` (autoria humana) e é mesclado pelo gerador a cada regeneração; o restante deste arquivo é saída do extrator.

## Frase 3

O casamento exato só encontrou "fraqueza", compartilhada entre AVC e hipertensão, e empatou. O método casou "fala ficou enrolada" e "formigamento no lado esquerdo do corpo" pela janela de proximidade. A frase é contaminada: já sabíamos que ela falhava, então o acerto não prova que a janela generaliza.

## Frase 7

Os dois métodos deram hipertensão, e o gabarito esperava ambíguo. O AVC não pontua em "dor de cabeça" porque o termo do Ministério é "dor de cabeça súbita" — a característica que distingue clinicamente a cefaleia do AVC. Conta como erro pelo critério pré-registrado, mas o resultado do sistema é clinicamente defensável, e o gabarito pode ter sido o julgamento mais fraco.

## Frase 9

A negação funcionou — "dor no peito" saiu negada. Mas "formigando" não casou porque o casamento respeita a oração, e AVC saiu com confiança baixa. Limitação de desenho documentada.

## Frase 10

Infarto com baixa confiança e 1 sintoma, como esperado. É o perfil em que o Ministério alerta que o infarto pode ocorrer sem sinais específicos.
