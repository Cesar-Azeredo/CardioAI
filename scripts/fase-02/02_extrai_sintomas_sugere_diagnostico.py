"""Extrator de sintomas e sugestao de diagnostico — Fase 2.

Implementa o protocolo pre-registrado e congelado em
document/fase-02/protocolo-extrator.md. Nenhuma regra deste arquivo existe
fora do protocolo; o numero entre colchetes em cada bloco ([2.5], [3.2] ...)
e a secao do protocolo que ele implementa.

Uso:
    python scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py
        roda nas 10 frases congeladas e grava document/fase-02/resultado-extrator.md
    python scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py --frase "texto"
        analisa uma frase avulsa (so imprime; nao grava nada)

Simulacao academica (FIAP — CardioIA, Fase 2). Sem validade para diagnostico
ou decisao medica.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import nltk

RAIZ = Path(__file__).resolve().parents[2]
MAPA_PATH = RAIZ / "document" / "datasets" / "fase-02" / "mapa-conhecimento-sintomas.csv"
FRASES_PATH = RAIZ / "assets" / "textos" / "fase-02" / "frases-sintomas-pacientes.txt"
PROTOCOLO_PATH = RAIZ / "document" / "fase-02" / "protocolo-extrator.md"
RESULTADO_PATH = RAIZ / "document" / "fase-02" / "resultado-extrator.md"
EXPLICACOES_PATH = RAIZ / "document" / "fase-02" / "explicacoes-divergencia.md"  # autoria humana
TESTES_PATH = RAIZ / "scripts" / "fase-02" / "03_testa_extrator.py"

AVISO = "Simulação acadêmica (FIAP — CardioIA, Fase 2). Sem validade para diagnóstico ou decisão médica."

# ---------------------------------------------------------------------------
# CONFIGURACAO PRE-REGISTRADA (copiada do protocolo; nao ajustar)
# ---------------------------------------------------------------------------
INTERVALO_MAXIMO = 2                                            # [3.2]
NEGADORES_PRE = {"nao", "nem", "nunca", "sem"}                  # [4.1] sem acento
NEGADORES_POS = {"nenhum", "nenhuma"}                           # [4.1]
NEGADORES = NEGADORES_PRE | NEGADORES_POS
PONTUACAO_FRONTEIRA = r"[,.;:!?]"                               # [4.2]
PALAVRAS_FRONTEIRA = {"mas", "porem", "contudo", "entretanto", "todavia", "e"}  # [4.2] sem acento
TERMOS_DE_LOCALIZACAO = ["braço esquerdo"]                      # [6] conceito (Sintoma 1) do mapa
RADICAIS_DE_DOR = {"dor", "doend"}                              # [6]
TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*")                 # [1] hifen interno preservado

# [2.5] recursos da NLTK conferidos por SHA-256 (divergencia = aviso, nao interrupcao)
RECURSOS_NLTK = {
    "rslp": ("stemmers/rslp.zip", "f482f9666a2a76cdd4acab16b01a44b002550ebaac29906dbd5a1bbc281e4f8b"),
    "stopwords": ("corpora/stopwords.zip", "48c0e52d8b52546e827f53761fb30300c0ab94f70660d28bd65ba0a86270946b"),
}

# [10.2] gabarito (document/fase-02/gabarito-frases.md) e [10.3] contaminadas
GABARITO = {
    1: ("Infarto", None), 2: ("Infarto", None), 3: ("AVC", None), 4: ("AVC", None),
    5: ("Hipertensão", None), 6: ("Hipertensão", None),
    7: ("ambíguo:AVC+Hipertensão", None), 8: ("Infarto", None), 9: ("AVC", None),
    10: ("Infarto", "baixa"),
}
CONTAMINADAS = {
    1: "regra de localização (6) — a frase cita braço esquerdo ao lado de dor no peito",
    3: "janela de 2 tokens (3.2) — o casamento exato falha em \"minha fala ficou enrolada\"",
    10: "nível \"baixa\" = 1 conceito (8) — a frase tem um único termo casado literalmente",
}


# ---------------------------------------------------------------------------
# [2.5] Recursos da NLTK
# ---------------------------------------------------------------------------
def diretorio_nltk() -> Path:
    """CARDIOIA_NLTK_DATA, se definido; senao <raiz>/.cache/nltk_data, com a raiz
    resolvida pela localizacao deste arquivo (nao pelo diretorio atual)."""
    return Path(os.environ.get("CARDIOIA_NLTK_DATA") or RAIZ / ".cache" / "nltk_data").resolve()


def preparar_recursos_nltk() -> list[dict]:
    """Baixa (so se ausente) e confere cada recurso. Devolve um registro por
    recurso com hash esperado e encontrado; nunca interrompe por divergencia."""
    destino = diretorio_nltk()
    destino.mkdir(parents=True, exist_ok=True)
    if str(destino) not in nltk.data.path:
        nltk.data.path.insert(0, str(destino))
    registros = []
    for nome, (relativo, esperado) in RECURSOS_NLTK.items():
        arquivo = destino / relativo
        if not arquivo.exists():
            if not nltk.download(nome, download_dir=str(destino), quiet=True):
                raise RuntimeError(f"não foi possível baixar o recurso NLTK '{nome}' para {destino}")
        encontrado = hashlib.sha256(arquivo.read_bytes()).hexdigest()
        registro = {"recurso": nome, "arquivo": str(arquivo), "esperado": esperado,
                    "encontrado": encontrado, "confere": encontrado == esperado}
        if not registro["confere"]:
            aviso = (f"ATENÇÃO: recurso NLTK '{nome}' diferente do pré-registrado\n"
                     f"  esperado:   {esperado}\n  encontrado: {encontrado}\n"
                     f"  O extrator continua; a divergência vai para o cabeçalho do resultado.")
            print("\n" + "!" * 78 + "\n" + aviso + "\n" + "!" * 78 + "\n", file=sys.stderr)
        registros.append(registro)
    return registros


# ---------------------------------------------------------------------------
# [1] Normalizacao e [2] radicalizacao
# ---------------------------------------------------------------------------
def sem_acento(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


@dataclass
class Token:
    superficie: str   # minuscula, com acento (como na frase)
    forma: str        # minuscula, sem acento — usada no baseline e nos gatilhos
    radical: str      # radical RSLP calculado COM acento, depois sem acento [1]


class Normalizador:
    def __init__(self) -> None:
        from nltk.corpus import stopwords
        from nltk.stem import RSLPStemmer
        self.stemmer = RSLPStemmer()
        self.stopwords = set(stopwords.words("portuguese"))   # [3.1]

    def token(self, superficie: str) -> Token:
        return Token(superficie, sem_acento(superficie), sem_acento(self.stemmer.stem(superficie)))

    def tokens(self, texto: str) -> list[Token]:
        return [self.token(t) for t in TOKEN.findall(texto.lower())]

    def oracoes(self, texto: str) -> list[list[Token]]:
        """[4.2] Pontuacao e palavras de fronteira separam oracoes; a fronteira
        em si nao entra em nenhuma oracao."""
        oracoes: list[list[Token]] = []
        for pedaco in re.split(PONTUACAO_FRONTEIRA, texto.lower()):
            atual: list[Token] = []
            for tok in self.tokens(pedaco):
                if tok.forma in PALAVRAS_FRONTEIRA:
                    if atual:
                        oracoes.append(atual)
                    atual = []
                else:
                    atual.append(tok)
            if atual:
                oracoes.append(atual)
        return oracoes

    def e_conteudo(self, tok: Token) -> bool:
        """[3.1] Palavra de conteudo: nao e stopword, ou e marcador de negacao."""
        return tok.superficie not in self.stopwords or tok.forma in NEGADORES


# ---------------------------------------------------------------------------
# Mapa: termos e conceitos
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Entrada:
    linha: int        # linha do CSV (1 = cabecalho)
    doenca: str
    sintoma1: str     # Sintoma 1 da linha
    coluna: str       # "Sintoma 1" ou "Sintoma 2"
    termo: str


@dataclass
class Mapa:
    entradas_por_chave_metodo: dict[tuple, list[Entrada]]
    entradas_por_chave_baseline: dict[tuple, list[Entrada]]
    conceito: dict[tuple[str, str], str]   # (doenca, sintoma1) -> rotulo do conceito unido


def carregar_mapa(norm: Normalizador) -> Mapa:
    with MAPA_PATH.open(encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))

    por_metodo: dict[tuple, list[Entrada]] = {}
    por_baseline: dict[tuple, list[Entrada]] = {}
    for n, l in enumerate(linhas, start=2):
        for coluna in ("Sintoma 1", "Sintoma 2"):
            termo = l[coluna].strip()
            toks = norm.tokens(termo)
            entrada = Entrada(n, l["Doença Associada"], l["Sintoma 1"].strip(), coluna, termo)
            chave_m = tuple(t.radical for t in toks if norm.e_conteudo(t))   # [3.1]
            chave_b = tuple(t.forma for t in toks)                            # [10.1]
            por_metodo.setdefault(chave_m, []).append(entrada)
            por_baseline.setdefault(chave_b, []).append(entrada)

    # [7.1] conceitos ligados por linha "literal" sao unidos (componente conexo por doenca)
    pai: dict[tuple[str, str], tuple[str, str]] = {}

    def achar(x):
        pai.setdefault(x, x)
        while pai[x] != x:
            pai[x] = pai[pai[x]]
            x = pai[x]
        return x

    s1_por_doenca = {(l["Doença Associada"], l["Sintoma 1"].strip()) for l in linhas}
    for par in s1_por_doenca:
        achar(par)
    for l in linhas:
        d, s1, s2 = l["Doença Associada"], l["Sintoma 1"].strip(), l["Sintoma 2"].strip()
        if l["tipo_termo"] == "literal" and (d, s2) in s1_por_doenca:
            pai[achar((d, s1))] = achar((d, s2))
    grupos: dict[tuple, list[str]] = {}
    for par in sorted(s1_por_doenca):
        grupos.setdefault(achar(par), []).append(par[1])
    conceito = {par: " / ".join(sorted(grupos[achar(par)])) for par in s1_por_doenca}
    return Mapa(por_metodo, por_baseline, conceito)


# ---------------------------------------------------------------------------
# [3] Casamento, [5] sobreposicao, [4] negacao, [6] localizacao
# ---------------------------------------------------------------------------
@dataclass
class Casamento:
    chave: tuple
    posicoes: tuple[int, ...]      # tokens consumidos [3.3]
    entradas: list[Entrada]
    oracao: int
    tokens_frase: str = ""
    negado_por: str | None = None
    dor_na_oracao: bool = True

    def conta(self, e: Entrada) -> bool:
        """[6] Entrada de conceito de localizacao so conta com dor nao negada na oracao."""
        return self.negado_por is None and (e.sintoma1 not in TERMOS_DE_LOCALIZACAO or self.dor_na_oracao)

    @property
    def localizacao_descartada(self) -> bool:
        return self.negado_por is None and not any(self.conta(e) for e in self.entradas)


def ocorrencias_metodo(radicais: list[str], chave: tuple) -> list[tuple[int, ...]]:
    """[3.2]/[3.3] Proximidade ordenada: cada palavra de conteudo seguinte a no
    maximo INTERVALO_MAXIMO tokens da anterior; ocorrencia mais a esquerda e mais
    curta; ocorrencias do mesmo termo sem sobreposicao."""
    achadas = []
    for inicio, r in enumerate(radicais):
        if r != chave[0]:
            continue
        pos = [inicio]
        for c in chave[1:]:
            limite = min(len(radicais), pos[-1] + 2 + INTERVALO_MAXIMO)
            proxima = next((q for q in range(pos[-1] + 1, limite) if radicais[q] == c), None)
            if proxima is None:
                break
            pos.append(proxima)
        else:
            achadas.append(tuple(pos))
    return _sem_sobreposicao(achadas)


def ocorrencias_baseline(formas: list[str], chave: tuple) -> list[tuple[int, ...]]:
    """[10.1] Sequencia exata e contigua de todos os tokens do termo."""
    k = len(chave)
    achadas = [tuple(range(i, i + k)) for i in range(len(formas) - k + 1) if tuple(formas[i:i + k]) == chave]
    return _sem_sobreposicao(achadas)


def _sem_sobreposicao(achadas):
    escolhidas, usados = [], set()
    for p in achadas:
        if not usados & set(p):
            escolhidas.append(p)
            usados |= set(p)
    return escolhidas


def gatilhos_nao_consumidos(oracao: list[Token], consumidos: set[int]) -> list[tuple[int, str]]:
    """[4.3] Um marcador so e gatilho se nao foi consumido por casamento aceito."""
    return [(i, t.forma) for i, t in enumerate(oracao) if t.forma in NEGADORES and i not in consumidos]


def gatilho_que_nega(inicio: int, fim: int, gatilhos: list[tuple[int, str]]) -> str | None:
    """[4.1]/[4.3] Pre-negacao antes do casamento, pos-negacao depois, ou
    qualquer gatilho dentro do intervalo do casamento."""
    for pos, forma in gatilhos:
        if forma in NEGADORES_PRE and pos < inicio:
            return forma
        if forma in NEGADORES_POS and pos > fim:
            return forma
        if inicio < pos < fim:
            return forma
    return None


def analisar(texto: str, norm: Normalizador, mapa: Mapa, metodo: str) -> dict:
    """metodo = "metodo" (protocolo 2-3) ou "baseline" (protocolo 10.1)."""
    por_chave = mapa.entradas_por_chave_metodo if metodo == "metodo" else mapa.entradas_por_chave_baseline
    oracoes = norm.oracoes(texto)
    aceitos: list[Casamento] = []
    for o, oracao in enumerate(oracoes):
        radicais = [t.radical for t in oracao]
        formas = [t.forma for t in oracao]
        candidatos = []
        for chave, entradas in por_chave.items():
            achar = ocorrencias_metodo(radicais, chave) if metodo == "metodo" else ocorrencias_baseline(formas, chave)
            for pos in achar:
                candidatos.append(Casamento(chave, pos, entradas, o))
        # [5] mais palavras de conteudo, depois menor extensao, depois posicao
        candidatos.sort(key=lambda c: (-len(c.chave), c.posicoes[-1] - c.posicoes[0], c.posicoes[0]))
        consumidos: set[int] = set()
        da_oracao = []
        for c in candidatos:
            if consumidos & set(c.posicoes):
                continue
            consumidos |= set(c.posicoes)
            c.tokens_frase = " ".join(oracao[i].superficie for i in c.posicoes)
            da_oracao.append(c)
        gatilhos = gatilhos_nao_consumidos(oracao, consumidos)
        for c in da_oracao:
            c.negado_por = gatilho_que_nega(c.posicoes[0], c.posicoes[-1], gatilhos)
        # [6] dor nao negada na oracao
        dor_na_oracao = any(
            t.radical in RADICAIS_DE_DOR and gatilho_que_nega(i, i, gatilhos) is None
            for i, t in enumerate(oracao)
        )
        for c in da_oracao:
            c.dor_na_oracao = dor_na_oracao
        aceitos.extend(da_oracao)

    # [7] pontuacao por conceitos distintos
    conceitos_por_doenca: dict[str, set[str]] = {}
    for c in aceitos:
        for e in c.entradas:
            if not c.conta(e):
                continue
            conceitos_por_doenca.setdefault(e.doenca, set()).add(mapa.conceito[(e.doenca, e.sintoma1)])
    pontuacao = {d: len(v) for d, v in conceitos_por_doenca.items()}
    sugestao, confianca = decidir(pontuacao)
    return {"texto": texto, "metodo": metodo, "casamentos": aceitos, "pontuacao": pontuacao,
            "conceitos": conceitos_por_doenca, "sugestao": sugestao, "confianca": confianca}


def decidir(pontuacao: dict[str, int]) -> tuple[list[str], str]:
    """[8] Niveis de confianca."""
    ordenadas = sorted(pontuacao.values(), reverse=True)
    p1 = ordenadas[0] if ordenadas else 0
    p2 = ordenadas[1] if len(ordenadas) > 1 else 0
    margem = p1 - p2
    if p1 == 0:
        return [], "sem sugestão"
    empatadas = sorted(d for d, v in pontuacao.items() if v == p1)
    if margem == 0:
        return empatadas, "ambíguo"
    if p1 == 1 and p2 == 0:
        return empatadas, "baixa"
    if p1 >= 3 and margem >= 2:
        return empatadas, "alta"
    return empatadas, "média"


# ---------------------------------------------------------------------------
# [10.2] Avaliacao
# ---------------------------------------------------------------------------
def rotulo(r: dict) -> str:
    if r["confianca"] == "sem sugestão":
        return "sem sugestão"
    if r["confianca"] == "ambíguo":
        return "ambíguo:" + "+".join(r["sugestao"])
    return r["sugestao"][0]


def acerto(n: int, r: dict) -> str:
    esperado_doenca, esperado_conf = GABARITO[n]
    ok_doenca = rotulo(r) == esperado_doenca
    if esperado_conf is None:
        return "acerto" if ok_doenca else "erro"
    ok_conf = r["confianca"] == esperado_conf
    return f"doença {'acerto' if ok_doenca else 'erro'}; confiança {'acerto' if ok_conf else 'erro'}"


# ---------------------------------------------------------------------------
# [9] Saida
# ---------------------------------------------------------------------------
def sha256(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def linhas_detalhe(r: dict) -> list[str]:
    out = []
    ok = [c for c in r["casamentos"] if not c.negado_por and not c.localizacao_descartada]
    neg = [c for c in r["casamentos"] if c.negado_por]
    loc = [c for c in r["casamentos"] if c.localizacao_descartada and not c.negado_por]

    def descreve(c: Casamento) -> str:
        termos = sorted({e.termo for e in c.entradas})
        por_doenca = {}
        for e in c.entradas:
            por_doenca.setdefault(e.doenca, set()).add(e.linha)
        onde = "; ".join(f"{d} (linha {', '.join(map(str, sorted(ls)))})" for d, ls in sorted(por_doenca.items()))
        return f"`{c.tokens_frase}` ← termo {' / '.join(repr(t) for t in termos)} — {onde}"

    out.append("- Termos casados:" + ("" if ok else " —"))
    out += [f"  - {descreve(c)}" for c in ok]
    out.append("- Termos negados:" + ("" if neg else " —"))
    out += [f"  - {descreve(c)} — gatilho `{c.negado_por}`" for c in neg]
    out.append("- Localização descartada (sem dor na oração):" + ("" if loc else " —"))
    out += [f"  - {descreve(c)}" for c in loc]
    if r["pontuacao"]:
        out.append("- Pontuação (conceitos distintos): " + "; ".join(
            f"{d} {v} ({', '.join(sorted(r['conceitos'][d]))})" for d, v in sorted(r["pontuacao"].items(), key=lambda x: (-x[1], x[0]))))
    else:
        out.append("- Pontuação (conceitos distintos): —")
    out.append(f"- **Sugestão: {', '.join(r['sugestao']) or '—'} — confiança {r['confianca']}**")
    return out


def ler_explicacoes() -> tuple[dict[int, str], str | None]:
    """Textos de autoria humana mesclados no relatorio (so escrita; nenhuma regra
    do protocolo depende disto). Devolve {frase: texto} e a nota abaixo da tabela."""
    if not EXPLICACOES_PATH.exists():
        return {}, None
    secoes: dict[str, list[str]] = {}
    atual = None
    for linha in EXPLICACOES_PATH.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            atual = linha[3:].strip()
            secoes[atual] = []
        elif atual is not None:
            secoes[atual].append(linha)
    textos = {int(nome.split()[1]): " ".join(l.strip() for l in corpo if l.strip())
              for nome, corpo in secoes.items() if nome.startswith("Frase ")}
    nota = "\n".join(secoes.get("Nota abaixo da tabela", [])).strip() or None
    return textos, nota


def relatorio(frases: list[str], resultados: list[tuple[dict, dict]], recursos: list[dict]) -> str:
    explicacoes, nota = ler_explicacoes()
    sem_texto = "—" if EXPLICACOES_PATH.exists() else "*(a escrever pelo grupo)*"
    agora = datetime.now().astimezone().isoformat(timespec="seconds")
    out = [
        "# Resultado do extrator de sintomas — Fase 2",
        "",
        f"> **{AVISO}**",
        "",
        "Arquivo **gerado** por `scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py`"
        " seguindo `document/fase-02/protocolo-extrator.md`. Não editar à mão.",
        "",
        "## Cabeçalho da execução",
        "",
        f"- Data: {agora}",
        f"- Protocolo `document/fase-02/protocolo-extrator.md`: `{sha256(PROTOCOLO_PATH)}`",
        f"- Mapa `document/datasets/fase-02/mapa-conhecimento-sintomas.csv`: `{sha256(MAPA_PATH)}`",
        f"- Frases `assets/textos/fase-02/frases-sintomas-pacientes.txt`: `{sha256(FRASES_PATH)}`",
        f"- Código `scripts/fase-02/02_extrai_sintomas_sugere_diagnostico.py`: `{sha256(Path(__file__))}`",
        f"- Testes `scripts/fase-02/03_testa_extrator.py`: `{sha256(TESTES_PATH) if TESTES_PATH.exists() else 'ausente'}`",
        f"- Python {sys.version.split()[0]}, nltk {nltk.__version__}",
        "- Recursos da NLTK (protocolo 2.5):",
    ]
    for rec in recursos:
        estado = "confere" if rec["confere"] else "**DIVERGE**"
        out.append(f"  - `{rec['recurso']}`: {estado} — esperado `{rec['esperado']}`, encontrado `{rec['encontrado']}`")
    out += ["", "## Avaliação (protocolo 10.4)", "",
            "| # | Gabarito | Baseline exato | Método | Acerto baseline | Acerto método | Contaminada | Explicação da divergência |",
            "|---|---|---|---|---|---|---|---|"]
    for n, (b, m) in enumerate(resultados, start=1):
        esperado = GABARITO[n][0] + (f", confiança {GABARITO[n][1]}" if GABARITO[n][1] else "")
        out.append(
            f"| {n} | {esperado} | {rotulo(b)} ({b['confianca']}) | {rotulo(m)} ({m['confianca']}) | "
            f"{acerto(n, b)} | {acerto(n, m)} | {'sim' if n in CONTAMINADAS else 'não'} | {explicacoes.get(n, sem_texto)} |")
    tot_b = sum(acerto(n, b).startswith(("acerto", "doença acerto")) for n, (b, _) in enumerate(resultados, 1))
    tot_m = sum(acerto(n, m).startswith(("acerto", "doença acerto")) for n, (_, m) in enumerate(resultados, 1))
    limpas = [n for n in range(1, len(resultados) + 1) if n not in CONTAMINADAS]
    lim_b = sum(acerto(n, resultados[n - 1][0]).startswith(("acerto", "doença acerto")) for n in limpas)
    lim_m = sum(acerto(n, resultados[n - 1][1]).startswith(("acerto", "doença acerto")) for n in limpas)
    if nota:
        out += ["", nota]
    out += ["",
            f"Acerto de doença — baseline exato: **{tot_b}/10**; método: **{tot_m}/10**.",
            f"Só nas frases não contaminadas ({', '.join(map(str, limpas))}) — baseline: **{lim_b}/{len(limpas)}**; método: **{lim_m}/{len(limpas)}**.",
            "",
            "Frases contaminadas (protocolo 10.3) — acerto do método nelas não conta como evidência a favor da decisão:",
            ""]
    out += [f"- Frase {n}: {motivo}" for n, motivo in CONTAMINADAS.items()]
    out += ["", "## Detalhe por frase (protocolo 9)", ""]
    for n, (b, m) in enumerate(resultados, start=1):
        out += [f"### Frase {n}", "", f"> {frases[n - 1]}", "", "**Método (RSLP + proximidade ordenada):**", ""]
        out += linhas_detalhe(m)
        out += ["", "**Baseline exato:**", ""]
        out += linhas_detalhe(b)
        out += ["", f"*{AVISO}*", ""]
    return "\n".join(out)


def resumo_terminal(n, texto, b, m) -> str:
    return (f"[{n:>2}] método: {', '.join(m['sugestao']) or '—'} ({m['confianca']}) {m['pontuacao']}\n"
            f"     baseline: {', '.join(b['sugestao']) or '—'} ({b['confianca']}) {b['pontuacao']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--frase", help="analisa uma frase avulsa (só imprime)")
    args = parser.parse_args()

    recursos = preparar_recursos_nltk()
    norm = Normalizador()
    mapa = carregar_mapa(norm)
    print(AVISO)

    if args.frase:
        m = analisar(args.frase, norm, mapa, "metodo")
        b = analisar(args.frase, norm, mapa, "baseline")
        print("\n".join(["", "Método:"] + linhas_detalhe(m) + ["", "Baseline exato:"] + linhas_detalhe(b)))
        return 0

    frases = [l for l in FRASES_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    resultados = []
    for n, frase in enumerate(frases, start=1):
        b = analisar(frase, norm, mapa, "baseline")
        m = analisar(frase, norm, mapa, "metodo")
        resultados.append((b, m))
        print(resumo_terminal(n, frase, b, m))
    RESULTADO_PATH.write_text(relatorio(frases, resultados, recursos) + "\n", encoding="utf-8")
    print(f"\nResultado gravado em {RESULTADO_PATH.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
