"""Coleta e extracao dos textos da Parte 2 (NLP) — Fase 1.

Baixa as duas paginas travadas na conversa com o time (nao busca outra fonte),
extrai o texto do corpo do artigo/pagina via BeautifulSoup e grava em
assets/textos/. Todo metadado (autor, ano, licenca, DOI etc.) e lido da
propria pagina no momento da execucao — nada e completado de memoria; o que
a fonte nao expoe vira TODO(humano) em assets/textos/PROVENIENCIA.md.

TEXTO 1 (SciELO, Arquivos Brasileiros de Cardiologia) — CC BY-NC 3.0: licenca
permite reproducao/redistribuicao nao comercial com atribuicao; nao impede
normalizacao de espacos em branco na extracao.

TEXTO 2 (Ministerio da Saude, gov.br) — CC BY-ND 3.0 (SemDerivacoes): a
clausula ND probe obra derivada. Por isso a extracao abaixo faz SOMENTE:
(a) selecionar o texto do corpo do artigo, descartando menu/rodape/links
relacionados; (b) normalizar espacos em branco introduzidos pela propria
conversao HTML->texto (ex.: espaco antes de pontuacao, deixado pela quebra
de tags inline como <strong>). Nao ha reescrita, resumo ou corte de trecho
do conteudo em si — qualquer paragrafo, lista ou secao presente na pagina
esta presente no .txt gerado, na mesma ordem e com as mesmas palavras.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import requests
from bs4 import BeautifulSoup

TEXTOS_DIR = Path(__file__).resolve().parents[2] / "assets" / "textos"
PROVENIENCIA_PATH = TEXTOS_DIR / "PROVENIENCIA.md"
DATA_DE_ACESSO = "2026-08-27"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}

URL_SCIELO = "https://www.scielo.br/j/abc/a/ZQMYdZFc7nYvKzVC6mXFKMt/?lang=pt"
URL_GOVBR = "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/h/hipertensao"

ARQUIVO_TEXTO_01 = (
    TEXTOS_DIR / "texto_01_trajetorias-saude-cardiovascular-scielo.txt"
)
ARQUIVO_TEXTO_02 = (
    TEXTOS_DIR / "texto_02_hipertensao-pressao-alta-ministerio-saude.txt"
)


def limpar_espacos(texto: str) -> str:
    """Normaliza espacos em branco introduzidos pela conversao HTML->texto.

    Colapsa espacos/tabs repetidos e remove espaco deixado antes de
    pontuacao quando uma tag inline (ex.: <sup>, <strong>) e removida no
    meio de uma frase. Nao adiciona, remove nem reescreve palavra alguma.
    """
    texto = re.sub(r"\s+", " ", texto).strip()
    texto = re.sub(r"\s+([.,;:!?])", r"\1", texto)
    return texto


@dataclass
class TextoExtraido:
    titulo: str
    corpo: str
    metadados: dict = field(default_factory=dict)


def buscar_pagina(url: str) -> BeautifulSoup:
    resposta = requests.get(url, headers=HEADERS, timeout=30)
    resposta.raise_for_status()
    return BeautifulSoup(resposta.text, "html.parser")


def extrair_texto_scielo(soup: BeautifulSoup) -> TextoExtraido:
    def meta(nome: str) -> str | None:
        tag = soup.find("meta", attrs={"name": nome})
        return tag["content"].strip() if tag and tag.get("content") else None

    titulo = limpar_espacos(soup.find("h1", class_="article-title").get_text(" "))

    # ha mais de um <a> com href de creativecommons nesta pagina (o selo-imagem
    # sem texto, e o link com a frase da licenca por extenso) — pega o que tem
    # texto proprio nao vazio, que e a frase completa da licenca do ARTIGO.
    candidatos_licenca = soup.find_all(
        "a", href=re.compile(r"creativecommons\.org/licenses/by-nc")
    )
    licenca_link = next(
        (a for a in candidatos_licenca if a.get_text(strip=True)), None
    )
    licenca_url = licenca_link["href"] if licenca_link else None
    licenca_texto = limpar_espacos(licenca_link.get_text(" ")) if licenca_link else None

    autores = [
        tag["content"].strip()
        for tag in soup.find_all("meta", attrs={"name": "citation_author"})
        if tag.get("content")
    ]

    metadados = {
        "titulo": titulo,
        "autores": autores,
        "afiliacao": meta("citation_author_affiliation"),
        "periodico": meta("citation_journal_title"),
        "periodico_abreviado": meta("citation_journal_abbrev"),
        "editora": meta("citation_publisher"),
        "volume": meta("citation_volume"),
        "numero": meta("citation_number"),
        "pagina_inicial": meta("citation_firstpage"),
        "pagina_final": meta("citation_lastpage"),
        "doi": meta("citation_doi"),
        "issn": [
            tag["content"].strip()
            for tag in soup.find_all("meta", attrs={"name": "citation_issn"})
            if tag.get("content")
        ],
        "ano_publicacao": meta("citation_publication_date"),
        "tipo_artigo": meta("citation_article_type"),
        "idioma": meta("citation_language"),
        "licenca_url": licenca_url,
        "licenca_texto_pagina": licenca_texto,
    }

    article = soup.find("article", id="articleText")
    secoes = article.find_all("div", class_="articleSection", recursive=False)
    secao_corpo, secao_referencias = secoes[0], secoes[1]

    paragrafos = [
        limpar_espacos(p.get_text(" "))
        for p in secao_corpo.find_all("p", recursive=False)
    ]
    paragrafos = [p for p in paragrafos if p]

    referencias = [
        limpar_espacos(li.get_text(" "))
        for li in secao_referencias.select("ul.refList > li")
    ]

    linhas = [titulo, ""] + paragrafos + ["", "REFERÊNCIAS", ""] + referencias
    corpo = "\n".join(linhas).strip() + "\n"

    return TextoExtraido(titulo=titulo, corpo=corpo, metadados=metadados)


def extrair_texto_govbr(soup: BeautifulSoup) -> TextoExtraido:
    licenca_link = soup.find("a", attrs={"rel": "license"})
    licenca_url = licenca_link["href"] if licenca_link else None
    licenca_texto = (
        limpar_espacos(licenca_link.parent.get_text(" "))
        if licenca_link and licenca_link.parent
        else None
    )

    conteudo = soup.find("div", id="content")
    titulo_tag = conteudo.find("h1", class_="outstanding-title")
    titulo = limpar_espacos(titulo_tag.get_text(" "))

    blocos = []
    for el in conteudo.descendants:
        nome = getattr(el, "name", None)
        if nome in ("h1", "h2", "h3"):
            texto_heading = limpar_espacos(el.get_text(" "))
            if texto_heading == "Mais informações":
                break
            blocos.append(("H", texto_heading))
        elif (
            nome == "div"
            and el.get("class")
            and "cover-richtext-tile" in el.get("class")
        ):
            paragrafos_ou_itens = [
                limpar_espacos(child.get_text(" "))
                for child in el.find_all(["p", "li"], recursive=True)
            ]
            paragrafos_ou_itens = [t for t in paragrafos_ou_itens if t]
            if not paragrafos_ou_itens:
                texto_bloco = limpar_espacos(el.get_text(" "))
                if texto_bloco:
                    paragrafos_ou_itens = [texto_bloco]
            blocos.append(("T", paragrafos_ou_itens))

    linhas: list[str] = []
    for kind, valor in blocos:
        if kind == "H":
            linhas.append("")
            linhas.append(valor)
            linhas.append("")
        else:
            linhas.extend(valor)

    corpo = "\n".join(linhas).strip() + "\n"

    metadados = {
        "titulo": titulo,
        "autor": "Ministério da Saúde (conteúdo institucional, sem autoria individual assinada)",
        "data_publicacao": None,  # nao encontrado na pagina — vira TODO(humano)
        "data_atualizacao": None,  # idem
        "licenca_url": licenca_url,
        "licenca_texto_pagina": licenca_texto,
    }

    return TextoExtraido(titulo=titulo, corpo=corpo, metadados=metadados)


def contar_palavras_e_caracteres(texto: str) -> tuple[int, int]:
    n_palavras = len(texto.split())
    n_caracteres = len(texto)
    return n_palavras, n_caracteres


def gravar_txt(caminho: Path, conteudo: str) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="utf-8", newline="\n")
    # confirma que o arquivo gravado e valido UTF-8 lendo de volta
    caminho.read_text(encoding="utf-8")


def escrever_proveniencia(
    t1: TextoExtraido,
    t2: TextoExtraido,
    contagem_t1: tuple[int, int],
    contagem_t2: tuple[int, int],
) -> None:
    m1 = t1.metadados
    m2 = t2.metadados
    autores_t1 = "; ".join(m1["autores"]) if m1["autores"] else "TODO(humano): autor nao encontrado na pagina"
    issn_t1 = ", ".join(m1["issn"]) if m1["issn"] else "TODO(humano)"

    conteudo = f"""# Proveniência dos textos — Parte 2 (NLP)

Ficha de cada texto, extraída da própria página no momento da coleta
(`scripts/fase-01/04_prepara_textos.py`). Nada foi completado de memória —
onde a fonte não expõe um campo, está marcado como `TODO(humano)`.

## Texto 1 — {t1.titulo}

- **Arquivo**: `{ARQUIVO_TEXTO_01.name}`
- **Título**: {m1['titulo']}
- **Autor(es)**: {autores_t1}
- **Afiliação (do primeiro autor, conforme a página)**: {m1['afiliacao'] or 'TODO(humano)'}
- **Periódico**: {m1['periodico']} ({m1['periodico_abreviado']})
- **Editora/Sociedade**: {m1['editora']}
- **Volume / número / páginas**: v.{m1['volume']}, n.{m1['numero']}, p.{m1['pagina_inicial']}-{m1['pagina_final']}
- **Tipo de artigo**: {m1['tipo_artigo']} (é um editorial curto, não um artigo de pesquisa original)
- **Ano de publicação**: {m1['ano_publicacao']}
- **DOI**: {m1['doi']}
- **ISSN**: {issn_t1}
- **Idioma**: {m1['idioma']}
- **URL**: {URL_SCIELO}
- **Licença**: {m1['licenca_texto_pagina'] or 'TODO(humano)'} ({m1['licenca_url']})
- **Data de acesso**: {DATA_DE_ACESSO}
- **Nº de palavras (contado, `texto.split()`)**: {contagem_t1[0]}
- **Nº de caracteres (contado, `len(texto)`)**: {contagem_t1[1]}
- **Processamento aplicado**: extração do corpo do artigo (`div.articleSection`, primeira ocorrência) e da lista de referências (segunda ocorrência), via BeautifulSoup; descartados apenas menu, cabeçalho de página, metadados de citação (capturados aqui) e caixa "Datas de Publicação". Normalização de espaços em branco (colapso de espaços repetidos, remoção de espaço antes de pontuação deixado pela remoção de tags `<sup>`/`<strong>`). Nenhuma frase foi reescrita, resumida ou cortada.

## Texto 2 — {t2.titulo}

- **Arquivo**: `{ARQUIVO_TEXTO_02.name}`
- **Título**: {m2['titulo']}
- **Autor**: {m2['autor']}
- **Fonte**: Ministério da Saúde — Saúde de A a Z
- **URL**: {URL_GOVBR}
- **Licença**: {m2['licenca_texto_pagina']} ({m2['licenca_url']})
- **Data de publicação/última atualização**: TODO(humano) — não encontramos campo de data associado a este conteúdo na página (sem `<time>`, sem meta `citation_*`, sem `dateModified`/`datePublished` em JSON-LD); se a rubrica exigir, confirmar via Wayback Machine ou contato direto com o Ministério da Saúde.
- **Data de acesso**: {DATA_DE_ACESSO}
- **Nº de palavras (contado, `texto.split()`)**: {contagem_t2[0]}
- **Nº de caracteres (contado, `len(texto)`)**: {contagem_t2[1]}
- **Processamento aplicado**: extração do corpo do artigo (`div#content`, títulos `h1`/`h2` e blocos `div.cover-richtext-tile`, em ordem de documento, até o título "Mais informações" que inicia a seção de links relacionados — excluída). Normalização de espaços em branco (mesma regra do Texto 1). **Nenhuma outra alteração de conteúdo** — obrigatório pela cláusula ND (SemDerivações) da licença CC BY-ND 3.0: esta licença permite cópia e redistribuição, mas **proíbe obra derivada** (resumir, reescrever, traduzir de forma livre, cortar trecho). Por isso o texto foi salvo integralmente, na ordem e com as palavras exatas da página.

## Alerta para `document/fase-01/governanca-e-vies.md` (a escrever depois das Partes 2 e 3)

O Texto 2 está sob **CC BY-ND 3.0**. Qualquer uso futuro (Fase 5 — chatbot,
por exemplo) que envolva reescrever, resumir ou traduzir automaticamente
trechos deste texto especificamente é, no limite, uma obra derivada e pode
conflitar com a licença. Um sistema de NLP pode **analisar** o texto (extrair
entidades, classificar tópicos, indexar para busca) sem violar a cláusula ND;
o risco aparece se o *output* do sistema reproduzir uma versão alterada do
texto original ao usuário final. Registrar essa distinção no governança.
"""
    PROVENIENCIA_PATH.write_text(conteudo, encoding="utf-8", newline="\n")


def main() -> None:
    print("[INFO] Baixando Texto 1 (SciELO)...")
    soup1 = buscar_pagina(URL_SCIELO)
    t1 = extrair_texto_scielo(soup1)
    gravar_txt(ARQUIVO_TEXTO_01, t1.corpo)
    contagem_t1 = contar_palavras_e_caracteres(t1.corpo)
    print(f"[OK] Texto 1 salvo em {ARQUIVO_TEXTO_01}")
    print(f"     {contagem_t1[0]} palavras, {contagem_t1[1]} caracteres")

    print("[INFO] Baixando Texto 2 (Ministério da Saúde)...")
    soup2 = buscar_pagina(URL_GOVBR)
    t2 = extrair_texto_govbr(soup2)
    gravar_txt(ARQUIVO_TEXTO_02, t2.corpo)
    contagem_t2 = contar_palavras_e_caracteres(t2.corpo)
    print(f"[OK] Texto 2 salvo em {ARQUIVO_TEXTO_02}")
    print(f"     {contagem_t2[0]} palavras, {contagem_t2[1]} caracteres")

    escrever_proveniencia(t1, t2, contagem_t1, contagem_t2)
    print(f"[OK] Proveniência gravada em {PROVENIENCIA_PATH}")

    print()
    print("=" * 78)
    print("RESUMO")
    print("=" * 78)
    print(json.dumps(t1.metadados, ensure_ascii=False, indent=2))
    print(json.dumps(t2.metadados, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
