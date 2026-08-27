# Proveniência dos textos — Parte 2 (NLP)

Ficha de cada texto, extraída da própria página no momento da coleta
(`scripts/fase-01/04_prepara_textos.py`). Nada foi completado de memória —
onde a fonte não expõe um campo, está marcado como `TODO(humano)`.

## Texto 1 — Trajetórias da Saúde Cardiovascular: Epidemiologia do Curso da Vida no Brasil

- **Arquivo**: `texto_01_trajetorias-saude-cardiovascular-scielo.txt`
- **Título**: Trajetórias da Saúde Cardiovascular: Epidemiologia do Curso da Vida no Brasil
- **Autor(es)**: Pellanda, Lucia Campos
- **Afiliação (do primeiro autor, conforme a página)**: Fundação Universitária de Cardiologia
- **Periódico**: Arquivos Brasileiros de Cardiologia (Arq. Bras. Cardiol.)
- **Editora/Sociedade**: Sociedade Brasileira de Cardiologia - SBC
- **Volume / número / páginas**: v.102, n.5, p.418-419
- **Tipo de artigo**: editorial (é um editorial curto, não um artigo de pesquisa original)
- **Ano de publicação**: 2014
- **DOI**: 10.5935/abc.20140065
- **ISSN**: 0066-782X, 1678-4170
- **Idioma**: pt
- **URL**: https://www.scielo.br/j/abc/a/ZQMYdZFc7nYvKzVC6mXFKMt/?lang=pt
- **Licença**: This is an Open Access article distributed under the terms of the Creative Commons Attribution Non-Commercial License which permits unrestricted non-commercial use, distribution, and reproduction in any medium, provided the original work is properly cited. (http://creativecommons.org/licenses/by-nc/3.0/)
- **Data de acesso**: 2026-08-27
- **Nº de palavras (contado, `texto.split()`)**: 1608
- **Nº de caracteres (contado, `len(texto)`)**: 10790
- **Processamento aplicado**: extração do corpo do artigo (`div.articleSection`, primeira ocorrência) e da lista de referências (segunda ocorrência), via BeautifulSoup; descartados apenas menu, cabeçalho de página, metadados de citação (capturados aqui) e caixa "Datas de Publicação". Normalização de espaços em branco (colapso de espaços repetidos, remoção de espaço antes de pontuação deixado pela remoção de tags `<sup>`/`<strong>`). Nenhuma frase foi reescrita, resumida ou cortada.

## Texto 2 — Hipertensão (pressão alta)

- **Arquivo**: `texto_02_hipertensao-pressao-alta-ministerio-saude.txt`
- **Título**: Hipertensão (pressão alta)
- **Autor**: Ministério da Saúde (conteúdo institucional, sem autoria individual assinada)
- **Fonte**: Ministério da Saúde — Saúde de A a Z
- **URL**: https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/h/hipertensao
- **Licença**: Todo o conteúdo deste site está publicado sob a licença Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada. (https://creativecommons.org/licenses/by-nd/3.0/deed.pt_BR)
- **Data de publicação/última atualização**: TODO(humano) — não encontramos campo de data associado a este conteúdo na página (sem `<time>`, sem meta `citation_*`, sem `dateModified`/`datePublished` em JSON-LD); se a rubrica exigir, confirmar via Wayback Machine ou contato direto com o Ministério da Saúde.
- **Data de acesso**: 2026-08-27
- **Nº de palavras (contado, `texto.split()`)**: 858
- **Nº de caracteres (contado, `len(texto)`)**: 5547
- **Processamento aplicado**: extração do corpo do artigo (`div#content`, títulos `h1`/`h2` e blocos `div.cover-richtext-tile`, em ordem de documento, até o título "Mais informações" que inicia a seção de links relacionados — excluída). Normalização de espaços em branco (mesma regra do Texto 1). **Nenhuma outra alteração de conteúdo** — obrigatório pela cláusula ND (SemDerivações) da licença CC BY-ND 3.0: esta licença permite cópia e redistribuição, mas **proíbe obra derivada** (resumir, reescrever, traduzir de forma livre, cortar trecho). Por isso o texto foi salvo integralmente, na ordem e com as palavras exatas da página.

## Alerta para `document/fase-01/governanca-e-vies.md` (a escrever depois das Partes 2 e 3)

O Texto 2 está sob **CC BY-ND 3.0**. Qualquer uso futuro (Fase 5 — chatbot,
por exemplo) que envolva reescrever, resumir ou traduzir automaticamente
trechos deste texto especificamente é, no limite, uma obra derivada e pode
conflitar com a licença. Um sistema de NLP pode **analisar** o texto (extrair
entidades, classificar tópicos, indexar para busca) sem violar a cláusula ND;
o risco aparece se o *output* do sistema reproduzir uma versão alterada do
texto original ao usuário final. Registrar essa distinção no governança.
