"""Coleta das fontes do mapa de conhecimento sintoma -> doenca — Fase 2.

Baixa as duas paginas gov.br travadas na decisao 1 da Fase 2 (secao 5bis do
CLAUDE.md/AGENTS.md) — nao busca outra fonte —, extrai o texto do corpo da
pagina e grava em assets/textos/fase-02/. Todo metadado (titulo, licenca) e
lido da propria pagina no momento da execucao; o que a fonte nao expoe fica
registrado como ausente em assets/textos/fase-02/PROVENIENCIA.md. A
proveniencia dos textos da Fase 1 (assets/textos/PROVENIENCIA.md) e gerada
por scripts/fase-01/04_prepara_textos.py e nao e tocada aqui.

Hipertensao nao e baixada: a fonte e o Texto 2 da Fase 1, ja no repositorio.

PAGINAS gov.br (Saude de A a Z) — CC BY-ND 3.0 (SemDerivacoes), mesma
restricao do Texto 2. A extracao faz SOMENTE: (a) selecionar o texto dos
blocos de conteudo da pagina, descartando menu, rodape e blocos de
Ouvidoria/selos; (b) normalizar espacos em branco da conversao HTML->texto.
Nenhuma reescrita, resumo, corte ou deduplicacao — inclusive paragrafos que a
propria pagina repete (a de infarto repete itens da lista de sintomas) ficam
repetidos, porque remover repeticao ja e alterar a obra. A funcao
`verificar_integridade` prova isso a cada execucao: o multiconjunto de
palavras do .txt tem que ser identico ao dos blocos de conteudo da pagina.

Diferencas deliberadas em relacao ao extrator da Fase 1
(`extrair_texto_govbr` em 04_prepara_textos.py), achadas ao rodar aquele
extrator nas paginas novas — o da Fase 1 continua correto para o Texto 2, que
nao tem esses casos, e nao foi alterado:
  1. blocos `outstanding-header` sem titulo (botoes com link, ex.: "Ligue 192
     SAMU") eram ignorados, truncando a frase "Se sentir dor no peito, suor
     frio, palidez e sensacao de desmaio," que continua nesse botao;
  2. um <h2> DENTRO de um bloco de texto saia depois do conteudo do bloco
     (ex.: "Saiba como funciona:"), invertendo a ordem do documento.

FONTES COMPLEMENTARES DA BVS/MS — fora do escopo (decisao do humano em
2026-09-23). As duas paginas (bvsms.saude.gov.br/ataque-cardiaco-infarto/ e
/avc-acidente-vascular-cerebral/) estavam inacessiveis: HTTP 503 ("The
requested URL was rejected", WAF F5) em todo o dominio, inclusive a home,
verificado por script e por navegador real. Como eram complementares e o
gov.br ja cobre as duas doencas, foram retiradas — e este script nao tenta
mais baixa-las, para nao depender de dominio fora do ar. Registro em
assets/textos/fase-02/PROVENIENCIA.md e document/fase-02/.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag

RAIZ = Path(__file__).resolve().parents[2]
TEXTOS_DIR = RAIZ / "assets" / "textos" / "fase-02"
PROVENIENCIA_PATH = TEXTOS_DIR / "PROVENIENCIA.md"
DATA_DE_ACESSO = date.today().isoformat()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}

BLOCOS_TEXTO = ("h1", "h2", "h3", "h4", "p", "li")


@dataclass
class Fonte:
    chave: str
    doenca: str
    url: str
    arquivo: str


FONTES = [
    Fonte(
        "infarto-govbr",
        "infarto",
        "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto",
        "texto_03_infarto-ministerio-saude.txt",
    ),
    Fonte(
        "avc-govbr",
        "AVC",
        "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/avc",
        "texto_04_avc-ministerio-saude.txt",
    ),
]


def limpar_espacos(texto: str) -> str:
    """Mesma regra do extrator da Fase 1: colapsa espacos e remove espaco
    antes de pontuacao deixado por tag inline. Nao mexe em palavra alguma."""
    texto = re.sub(r"\s+", " ", texto).strip()
    texto = re.sub(r"\s+([.,;:!?])", r"\1", texto)
    return texto


@dataclass
class TextoExtraido:
    titulo: str
    corpo: str
    metadados: dict = field(default_factory=dict)
    texto_blocos: str = ""  # texto bruto dos blocos, para a verificacao


@dataclass
class ResultadoColeta:
    fonte: Fonte
    texto: TextoExtraido
    contagem: tuple[int, int]


def blocos_de_conteudo(conteudo: Tag) -> list[Tag]:
    """Blocos de conteudo editorial da pagina, em ordem de documento.

    `cover-richtext-tile` (texto) e `outstanding-header` (titulos e botoes).
    Para no primeiro `cover-embed-tile` (Ouvidoria, selos, rodape) ou no
    titulo "Mais informacoes" (links relacionados), como na Fase 1.
    """
    blocos = []
    for div in conteudo.find_all("div", class_="tile-content"):
        classes = div.get("class", [])
        if "cover-embed-tile" in classes:
            break
        if limpar_espacos(div.get_text(" ")) == "Mais informações":
            break
        if "cover-richtext-tile" in classes or "outstanding-header" in classes:
            blocos.append(div)
    return blocos


def linhas_do_bloco(bloco: Tag) -> list[tuple[str, str]]:
    """Linhas de um bloco, em ordem. Pega so elementos-folha (um <li> que
    contem <p> vira uma linha so, sem duplicar). Titulo vira ("H", texto)."""
    folhas = [
        el
        for el in bloco.find_all(BLOCOS_TEXTO)
        if not el.find(BLOCOS_TEXTO)
    ]
    if not folhas:
        # botao/link sem elemento de bloco (ex.: "Ligue 192 SAMU")
        texto = limpar_espacos(bloco.get_text(" "))
        return [("T", texto)] if texto else []
    linhas = []
    for el in folhas:
        texto = limpar_espacos(el.get_text(" "))
        if texto:
            linhas.append(("H" if el.name.startswith("h") else "T", texto))
    return linhas


def extrair_texto_govbr(soup: BeautifulSoup) -> TextoExtraido:
    licenca_link = soup.find("a", attrs={"rel": "license"})
    licenca_url = licenca_link["href"] if licenca_link else None
    licenca_texto = (
        limpar_espacos(licenca_link.parent.get_text(" "))
        if licenca_link and licenca_link.parent
        else None
    )

    conteudo = soup.find("div", id="content")
    titulo = limpar_espacos(
        conteudo.find("h1", class_="outstanding-title").get_text(" ")
    )

    blocos = blocos_de_conteudo(conteudo)
    saida: list[str] = []
    for bloco in blocos:
        for tipo, texto in linhas_do_bloco(bloco):
            if tipo == "H":
                saida.extend(["", texto, ""])
            else:
                saida.append(texto)
    corpo = re.sub(r"\n{3,}", "\n\n", "\n".join(saida)).strip() + "\n"

    metadados = {
        "titulo": titulo,
        "autor": "Ministério da Saúde (conteúdo institucional, sem autoria individual assinada)",
        "data_publicacao": None,
        "licenca_url": licenca_url,
        "licenca_texto_pagina": licenca_texto,
        "n_blocos": len(blocos),
    }
    texto_blocos = " ".join(b.get_text(" ") for b in blocos)
    return TextoExtraido(titulo, corpo, metadados, texto_blocos)


def verificar_integridade(t: TextoExtraido) -> None:
    """Prova de nao-derivacao (clausula ND): o .txt contem exatamente as
    mesmas palavras, com as mesmas repeticoes, que os blocos de conteudo da
    pagina — nada cortado, nada acrescentado, nada deduplicado."""
    pagina = Counter(limpar_espacos(t.texto_blocos).split())
    arquivo = Counter(t.corpo.split())
    if pagina != arquivo:
        faltando = pagina - arquivo
        sobrando = arquivo - pagina
        raise RuntimeError(
            f"extracao alterou o conteudo de '{t.titulo}': "
            f"faltando={dict(faltando)} sobrando={dict(sobrando)}"
        )


def data_exposta_na_pagina(soup: BeautifulSoup) -> bool:
    """Mesma checagem registrada para o Texto 2: <time>, meta citation_* de
    data e dateModified/datePublished em JSON-LD."""
    if soup.find("time"):
        return True
    if soup.find("meta", attrs={"name": re.compile(r"citation_.*date")}):
        return True
    return bool(re.search(r"date(Modified|Published)", str(soup)))


def repeticoes_da_fonte(corpo: str) -> list[tuple[str, int]]:
    """Linhas que a propria pagina repete — registradas, nao removidas."""
    linhas = [l for l in corpo.splitlines() if l.strip()]
    return [(l, n) for l, n in Counter(linhas).items() if n > 1]


def coletar(fonte: Fonte) -> ResultadoColeta:
    resposta = requests.get(fonte.url, headers=HEADERS, timeout=30)
    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")
    texto = extrair_texto_govbr(soup)
    verificar_integridade(texto)
    texto.metadados["data_exposta"] = data_exposta_na_pagina(soup)
    texto.metadados["repeticoes"] = repeticoes_da_fonte(texto.corpo)

    caminho = TEXTOS_DIR / fonte.arquivo
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto.corpo, encoding="utf-8", newline="\n")
    caminho.read_text(encoding="utf-8")  # confirma UTF-8 valido

    contagem = (len(texto.corpo.split()), len(texto.corpo))
    return ResultadoColeta(fonte, texto, contagem)


def ficha_coletada(r: ResultadoColeta) -> str:
    m = r.texto.metadados
    if m["data_exposta"]:
        data_pub = "TODO(humano): a página expõe um campo de data — conferir e registrar"
    else:
        data_pub = (
            "a página-fonte não expõe data de publicação nem de atualização "
            "(verificado: sem `<time>`, sem meta `citation_*`, sem "
            "`dateModified`/`datePublished` em JSON-LD) — a data de acesso é a "
            "referência temporal disponível."
        )
    if m["repeticoes"]:
        itens = "\n".join(
            f"  - {n}× — \"{linha[:90]}{'…' if len(linha) > 90 else ''}\""
            for linha, n in m["repeticoes"]
        )
        repeticoes = (
            "a própria página repete as linhas abaixo (conferido no HTML-fonte). "
            "**Mantidas repetidas no .txt** — remover repetição é alterar a "
            "obra (cláusula ND). Quem consumir este texto (mapa de "
            "conhecimento, contagem de termos) deve contar cada ocorrência "
            "uma vez só:\n" + itens
        )
    else:
        repeticoes = "nenhuma linha repetida na página."
    return f"""## Texto {int(r.fonte.arquivo.split('_')[1])} — {m['titulo']}

- **Arquivo**: `{r.fonte.arquivo}`
- **Doença coberta no mapa**: {r.fonte.doenca}
- **Título**: {m['titulo']}
- **Autor**: {m['autor']}
- **Fonte**: Ministério da Saúde — Saúde de A a Z
- **URL**: {r.fonte.url}
- **Licença**: {m['licenca_texto_pagina'] or 'TODO(humano): licença não encontrada na página'} ({m['licenca_url']})
- **Data de publicação/última atualização**: {data_pub}
- **Data de acesso**: {DATA_DE_ACESSO}
- **Nº de palavras (contado, `texto.split()`)**: {r.contagem[0]}
- **Nº de caracteres (contado, `len(texto)`)**: {r.contagem[1]}
- **Repetições da fonte**: {repeticoes}
- **Processamento aplicado**: extração dos {m['n_blocos']} blocos de conteúdo da página (`div.cover-richtext-tile` e `div.outstanding-header`, em ordem de documento, até o primeiro bloco de rodapé `cover-embed-tile`), um elemento-folha (`h1`–`h4`, `p`, `li`) por linha. Normalização de espaços em branco (mesma regra da Fase 1). **Nenhuma outra alteração** — obrigatório pela cláusula ND da CC BY-ND 3.0. Integridade verificada por script a cada execução: o multiconjunto de palavras do `.txt` é idêntico ao dos blocos de conteúdo da página.
"""


def escrever_proveniencia(resultados: list[ResultadoColeta]) -> None:
    fichas = "\n".join(ficha_coletada(r) for r in resultados)
    conteudo = f"""# Proveniência dos textos — Fase 2 (fontes do mapa de conhecimento)

Gerado por `scripts/fase-02/00_coleta_fontes_mapa.py`. Nada foi completado de
memória: metadado que a página não expõe está registrado como ausente.

O mapa de conhecimento cobre **três doenças** (decisão 1 da Fase 2, seção
5bis do `CLAUDE.md`/`AGENTS.md`):

| Doença | Fonte primária | Fonte complementar |
|---|---|---|
| Hipertensão | Texto 2 da Fase 1 — `assets/textos/texto_02_hipertensao-pressao-alta-ministerio-saude.txt` (ficha em `assets/textos/PROVENIENCIA.md`) | — |
| Infarto | Texto 3 (gov.br) | — |
| AVC | Texto 4 (gov.br) | — |

**Fontes complementares da BVS inacessíveis (HTTP 503 em todo o domínio,
verificado por script e navegador em 2026-09-23), retiradas do escopo.** Eram
as páginas `https://bvsms.saude.gov.br/ataque-cardiaco-infarto/` e
`https://bvsms.saude.gov.br/avc-acidente-vascular-cerebral/`; o servidor
respondeu com a página de bloqueio do WAF ("The requested URL was rejected")
para qualquer URL do domínio, inclusive a home. Nenhum conteúdo delas foi
lido, e portanto nenhuma linha do mapa se apoia nelas. A cobertura de infarto
e AVC vem inteira das páginas do gov.br (Saúde de A a Z), que são a fonte
primária.

**Restrição de licença (CC BY-ND 3.0 nas páginas do gov.br)**: estes textos
podem ser **analisados** (extrair termos de sintoma para o mapa, contar,
indexar), mas não reescritos, resumidos ou traduzidos livremente. O mapa de
conhecimento cita o trecho literal de onde cada sintoma saiu; as frases de
paciente da Fase 2 são redação própria do grupo, não paráfrase destes textos.

{fichas}"""
    PROVENIENCIA_PATH.write_text(conteudo, encoding="utf-8", newline="\n")


def main() -> int:
    resultados = []
    for fonte in FONTES:
        print(f"[INFO] {fonte.chave}: {fonte.url}")
        r = coletar(fonte)
        print(f"[OK]   {fonte.arquivo}: {r.contagem[0]} palavras, {r.contagem[1]} caracteres")
        for linha, n in r.texto.metadados["repeticoes"]:
            print(f"       repetida na fonte {n}x: {linha[:70]}...")
        resultados.append(r)

    escrever_proveniencia(resultados)
    print(f"[OK]   Proveniência gravada em {PROVENIENCIA_PATH.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
