"""Verificacao do dataset rotulado de risco e do conjunto-desafio — Fase 2, Parte 2.

Confere, por maquina, o que document/fase-02/criterio-rotulo-risco.md e a
ficha em document/datasets/fase-02/README.md prometem, e sai com codigo 1 se
alguma regra dura falhar:

  CONGELAMENTO  SHA-256 de frases-rotuladas-risco.csv e desafio-risco.csv
             tem que bater com o congelado — o dataset nao muda depois de
             revisado, nem para acomodar resultado do classificador.
  FORMATO    cabecalho frase,situacao (literal do enunciado) + extras depois;
             80 frases, 40 "alto risco" / 40 "baixo risco"; codigos de sinal.
  CRITERIO   todo trecho-fonte citado no criterio existe literalmente na pagina.
  SEGURANCA  nenhuma frase de baixo risco tem sinal de alerta presente: (a) o
             extrator da Parte 1 nao pode casar termo do mapa nao negado;
             (b) lista de palavras vedadas (criterio, secao 2), com o mesmo
             escopo de negacao do extrator; excecao so com revisao registrada.
  DIVERSIDADE >= 4 negacoes no baixo risco; >= 8 frases de baixo risco com
             palavra de corpo que tambem aparece no alto risco.
  REDACAO    sem digito nem "anos" (LGPD); clausula ND: maior sequencia de
             palavras em comum com as paginas-fonte < 6; nenhuma frase igual a
             uma das 10 frases da Parte 1.
  QUASE-DUPLICATA  cosseno TF-IDF (radicais de conteudo) entre todos os pares
             das 80, e entre 80 x desafio x 10 frases da Parte 1. Limiar
             calibrado no proprio dataset (ver limiar_quase_copia).
  ATALHO     para cada palavra de conteudo, em quantas frases de cada classe
             aparece; lista as 10 que so aparecem numa classe e em mais frases.
  GENERO     coluna marcador_genero (metadado autoral) conferida contra a
             concordancia com quem fala: adjetivo do lexico ate 4 tokens depois
             de verbo em 1a pessoa, na mesma oracao; >= 6 femininas e >= 6
             masculinas marcadas em cada classe do treino.
  CONTRAFACTUAL  no desafio, cada par_contrafactual tem 2 frases (feminino e
             masculino), mesmo rotulo, texto identico exceto a concordancia.
  FUNCIONAIS (INFORMATIVO — adicionado depois do achado do classificador)
             palavras funcionais (stopwords da NLTK) por classe, na MESMA
             representacao do TfidfVectorizer do notebook. A tabela ATALHO acima
             so via palavras de conteudo; o classificador mantem as stopwords, e
             "mas" (0 alto / 10 baixo) e "eu" (7 / 0) passaram pelo ponto cego.
             Nao reprova nada: o dataset continua congelado e a regra de parada
             do balanceamento nao se aplica retroativamente.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
TREINO_PATH = RAIZ / "document" / "datasets" / "fase-02" / "frases-rotuladas-risco.csv"
DESAFIO_PATH = RAIZ / "document" / "datasets" / "fase-02" / "desafio-risco.csv"
CRITERIO_PATH = RAIZ / "document" / "fase-02" / "criterio-rotulo-risco.md"
FRASES_P1_PATH = RAIZ / "assets" / "textos" / "fase-02" / "frases-sintomas-pacientes.txt"
T2 = "assets/textos/texto_02_hipertensao-pressao-alta-ministerio-saude.txt"
T3 = "assets/textos/fase-02/texto_03_infarto-ministerio-saude.txt"
T4 = "assets/textos/fase-02/texto_04_avc-ministerio-saude.txt"


def carregar(nome, arquivo):
    spec = importlib.util.spec_from_file_location(nome, AQUI / arquivo)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome] = mod
    spec.loader.exec_module(mod)
    return mod


ext = carregar("extrator", "02_extrai_sintomas_sugere_diagnostico.py")
verif = carregar("verificador", "01_verifica_mapa_e_frases.py")

# Dataset e desafio congelados em 2026-09-23, depois da revisao do grupo.
SHA256_TREINO_CONGELADO = "1f493de6da6a080845e278d1de2b773ce96ecefa442b94e3e69db5c37404e9da"
SHA256_DESAFIO_CONGELADO = "c38357f633461401e8857dab3b91cf521478ba9a4313b7ebddf5a53473222f15"
N_POR_CLASSE = 40
CLASSES = ("alto risco", "baixo risco")
CLASSES_DESAFIO = {"alto risco", "baixo risco", "indefinido"}
SINAIS = {"I1", "I2", "I3", "I4", "I5", "I6", "I7", "A1", "A2", "A3", "A4", "A5", "A6"}
TIPOS = {"infarto-literal", "infarto-leigo", "avc-literal", "avc-leigo", "combinado",
         "benigno-corpo", "benigno-negacao", "benigno-outro"}
TIPOS_DESAFIO = {"desafio-negacao", "desafio-atipico", "desafio-zona", "desafio-vocabulario", "desafio-genero"}
MIN_GENERO_POR_CLASSE = 6
# Formas que concordam em genero com quem fala ("eu"), usadas nos dois conjuntos.
GENERO_FEM = {"assustada", "encharcada", "sentada", "obrigada", "confusa", "pálida", "quebrada", "moída",
              "congestionada", "empolgada", "estressada", "cansada", "gripada", "esquisita", "suada",
              "diabética", "estranha"}
GENERO_MAS = {"gelado", "molhado", "branco", "parado", "sozinho", "tonto", "desorientado", "preocupado",
              "resfriado", "cansado", "sonolento", "travado", "animado", "envergonhado", "chateado",
              "esquisito", "gripado", "suado", "pálido", "diabético"}
VERBOS_1A_PESSOA = {"estou", "to", "fiquei", "ficar", "sou", "estava", "voltei", "acordei", "fico", "ando",
                    "fui", "cheguei", "descanso", "sentindo"}
JANELA_GENERO = 4
MIN_NEGACAO_BAIXO = 4
MIN_CORPO_BAIXO = 8

# Trechos citados em document/fase-02/criterio-rotulo-risco.md (conferidos na pagina e no criterio)
TRECHOS = [
    (T3, "Tratamento: Infarto é uma emergência que exige cuidados médicos imediatos."),
    (T3, "Se sentir dor no peito, suor frio, palidez e sensação de desmaio,"),
    (T3, "Ligue 192 SAMU"),
    (T3, "Ou procure uma Emergência Cardiológica mais próxima."),
    (T3, "Dor ou desconforto na região peitoral, podendo irradiar para as costas, rosto, braço esquerdo e, raramente, braço direito."),
    (T3, "acompanhada de sensação de peso ou aperto sobre o tórax"),
    (T3, "provocando suor frio, palidez, falta de ar e sensação de desmaio."),
    (T3, "Em idosos, o principal sintoma do infarto agudo do miocárdio pode ser a falta de ar."),
    (T3, "Nos diabéticos e idosos, o infarto também pode ocorrer sem sinais específicos. Por isso, deve-se estar atento a qualquer mal-estar súbito."),
    (T3, "A dor também pode ser no abdome, semelhante a dor de uma gastrite ou esofagite de refluxo, mas é pouco frequente."),
    (T4, "Os principais sinais de alerta para qualquer tipo de AVC são:"),
    (T4, "Importante: Caso qualquer um desses sintomas apareçam, é fundamental ligar para o Serviço de Atendimento Médico de Urgência (SAMU - 192), Bombeiros (193) ou levar a pessoa imediatamente a um hospital para avaliação clínica detalhada."),
    (T4, "Confusão mental;"),
    (T4, "Alteração da falar ou compreensão;"),
    (T4, "Alteração na visão (em um ou ambos os olhos);"),
    (T4, "Dor de cabeça súbita, intensa, sem causa aparente;"),
    (T4, "Alteração do equilíbrio, coordenação, tontura ou alteração no andar;"),
    (T4, "Fraqueza ou formigamento em um lado do corpo (rosto, braço ou perna)."),
    (T2, "Os sintomas da hipertensão costumam aparecer somente quando a pressão sobe muito: podem ocorrer dores no peito, dor de cabeça, tonturas, zumbido no ouvido, fraqueza, visão embaçada e sangramento nasal."),
    (T2, "Medir a pressão regularmente é a única maneira de diagnosticar a hipertensão."),
]

# Criterio, secao 2: palavras vedadas no baixo risco quando NAO negadas (sinais de
# alerta, zona cinzenta e exclusoes de seguranca). Comparadas por radical RSLP.
VEDADAS_BAIXO = [
    "peito", "tórax", "suor", "suando", "suei", "palidez", "pálido", "pálida", "falta", "ar",
    "fôlego", "desmaio", "desmaiar", "mal-estar", "confusão", "confuso", "desorientado",
    "fala", "falar", "visão", "vista", "enxergando", "olho", "equilíbrio", "tontura", "tonto",
    "rodar", "andar", "formigamento", "formigando", "dormente", "dormência", "fraqueza",
    "fraco", "fraca", "cabeça", "zumbido", "zumbir", "sangue", "sangramento",
    "abdome", "barriga", "estômago", "azia", "náusea", "enjoo", "vômito", "vomitei",
    "palpitação", "coração",
]
# Ocorrencias revisadas e aceitas (frase exata, palavra, motivo). Toda excecao e registrada.
EXCECOES_REVISADAS = {
    ("Cortei a mão descascando batata, sangrou um pouco mas já estancou com o curativo.", "sangrou"):
        "sangramento de corte na mão, com causa e já estancado — não é sangramento nasal (zona cinzenta)",
    ("Dormi de mau jeito e acordei com o pescoço duro; virar para o lado ainda incomoda.", "dormi"):
        "over-stemming do RSLP: dormir (sono) e dormente/dormência têm o mesmo radical `dorm`; a frase fala de sono",
}
CORPO = ["peito", "tórax", "braço", "braços", "costas", "perna", "pernas", "rosto", "cabeça",
         "corpo", "lado", "mão", "queixo", "ombro", "pescoço", "pé", "olho", "joelho"]


def ler_csv(caminho):
    with caminho.open(encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        return leitor.fieldnames, list(leitor)


def conteudo(norm, texto):
    return [t.radical for t in norm.tokens(texto) if norm.e_conteudo(t)]


def tokens_nao_negados(norm, texto):
    """Tokens fora de escopo de negacao, com as mesmas regras do extrator
    (oracao, gatilhos pre e pos). Nenhum termo e consumido aqui."""
    for oracao in norm.oracoes(texto):
        gat = ext.gatilhos_nao_consumidos(oracao, set())
        for i, t in enumerate(oracao):
            if t.forma in ext.NEGADORES:
                continue
            if ext.gatilho_que_nega(i, i, gat) is None:
                yield t


def genero_da_voz(norm, texto) -> tuple[str, list[str]]:
    """Genero marcado por concordancia com quem fala. Um adjetivo do lexico so
    conta se houver verbo em 1a pessoa ate JANELA_GENERO tokens antes dele, na
    mesma oracao — "suor gelado" ou "tomo algo gelado" nao marcam a voz."""
    achados = []
    for oracao in norm.oracoes(texto):
        for i, t in enumerate(oracao):
            if t.superficie in GENERO_FEM | GENERO_MAS and any(
                    oracao[j].forma in VERBOS_1A_PESSOA for j in range(max(0, i - JANELA_GENERO), i)):
                achados.append(t.superficie)
    f = [w for w in achados if w in GENERO_FEM]
    m = [w for w in achados if w in GENERO_MAS]
    if f and m:
        return "misto", achados
    return ("feminino" if f else "masculino" if m else "neutro"), achados


def chave_sem_genero(norm, texto):
    return [t.superficie[:-1] if t.superficie in GENERO_FEM | GENERO_MAS else t.superficie for t in norm.tokens(texto)]


def limiar_quase_copia(vet, docs):
    """Calibracao no proprio dataset: para cada frase e cada palavra de conteudo,
    o cosseno entre a frase e ela mesma sem aquela palavra (uma "edicao de uma
    palavra"). O limiar e a MEDIANA dessas similaridades: um par de frases
    diferentes acima dele e tao parecido quanto uma edicao tipica de uma
    palavra — isto e, quase copia."""
    sims = []
    for d in docs:
        if len(set(d)) < 2:
            continue
        base = vet.transform([d])
        for w in set(d):
            sims.append(cosine_similarity(base, vet.transform([[x for x in d if x != w]]))[0, 0])
    return statistics.median(sims), min(sims), max(sims)


def main() -> int:
    falhas = []
    recursos = ext.preparar_recursos_nltk()
    norm = ext.Normalizador()
    mapa = ext.carregar_mapa(norm)

    cab, treino = ler_csv(TREINO_PATH)
    cab_d, desafio = ler_csv(DESAFIO_PATH)
    frases_p1 = [l for l in FRASES_P1_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    criterio = CRITERIO_PATH.read_text(encoding="utf-8")

    print("=" * 78 + "\nCONGELAMENTO\n" + "=" * 78)
    for nome, caminho, esperado in (("treino", TREINO_PATH, SHA256_TREINO_CONGELADO),
                                    ("desafio", DESAFIO_PATH, SHA256_DESAFIO_CONGELADO)):
        sha = hashlib.sha256(caminho.read_bytes()).hexdigest()
        if sha != esperado:
            falhas.append(f"{nome} alterado: SHA-256 {sha[:12]}… ≠ congelado {esperado[:12]}…")
            print(f"[FALHA] {nome}: SHA-256 {sha[:12]}… ≠ congelado {esperado[:12]}…")
        else:
            print(f"[OK]    {nome} congelado (SHA-256 {sha[:12]}…)")

    print("\n" + "=" * 78 + "\nFORMATO\n" + "=" * 78)
    if cab[:2] != ["frase", "situacao"] or cab_d[:2] != ["frase", "situacao"]:
        falhas.append(f"cabeçalho: treino {cab[:2]}, desafio {cab_d[:2]} (esperado frase,situacao)")
    cont = Counter(l["situacao"] for l in treino)
    print(f"treino: {len(treino)} frases — {dict(cont)}; colunas {cab}")
    print(f"desafio: {len(desafio)} frases — {dict(Counter(l['situacao'] for l in desafio))}; colunas {cab_d}")
    if len(treino) != 2 * N_POR_CLASSE or any(cont[c] != N_POR_CLASSE for c in CLASSES) or set(cont) - set(CLASSES):
        falhas.append(f"treino precisa de {N_POR_CLASSE}/{N_POR_CLASSE} alto/baixo risco: {dict(cont)}")
    for conj, linhas, tipos, classes in (("treino", treino, TIPOS, set(CLASSES)), ("desafio", desafio, TIPOS_DESAFIO, CLASSES_DESAFIO)):
        for l in linhas:
            codigos = {c for c in l["sinal_de_alerta"].split(";") if c}
            if l["situacao"] not in classes:
                falhas.append(f"{conj}: situação inválida {l['situacao']!r}: {l['frase'][:50]}")
            if l["tipo_frase"] not in tipos:
                falhas.append(f"{conj}: tipo_frase inválido {l['tipo_frase']!r}")
            if l["situacao"] == "alto risco" and (not codigos or codigos - SINAIS):
                falhas.append(f"{conj}: alto risco sem código de sinal válido: {l['frase'][:50]}")
            if l["situacao"] == "baixo risco" and codigos:
                falhas.append(f"{conj}: baixo risco com sinal de alerta: {l['frase'][:50]}")

    print("\n" + "=" * 78 + "\nCRITÉRIO — trechos-fonte\n" + "=" * 78)
    ok_trechos = 0
    for fonte, trecho in TRECHOS:
        na_pagina = trecho in (RAIZ / fonte).read_text(encoding="utf-8")
        no_criterio = trecho in criterio
        ok_trechos += na_pagina and no_criterio
        if not (na_pagina and no_criterio):
            falhas.append(f"trecho {trecho[:50]!r}: na página={na_pagina}, no critério={no_criterio}")
    print(f"{ok_trechos}/{len(TRECHOS)} trechos existem literalmente na página e no critério")

    print("\n" + "=" * 78 + "\nSEGURANÇA — nenhum sinal de alerta presente no baixo risco\n" + "=" * 78)
    vedadas = {ext.sem_acento(norm.stemmer.stem(w)): w for w in VEDADAS_BAIXO}
    baixo = [l for l in treino if l["situacao"] == "baixo risco"]
    alto = [l for l in treino if l["situacao"] == "alto risco"]
    for l in baixo:
        r = ext.analisar(l["frase"], norm, mapa, "metodo")
        for c in r["casamentos"]:
            if c.negado_por is None and not c.localizacao_descartada:
                falhas.append(f"baixo risco com termo do mapa casado: `{c.tokens_frase}` em {l['frase'][:60]}")
        for t in tokens_nao_negados(norm, l["frase"]):
            if t.radical in vedadas:
                chave = (l["frase"], t.superficie)
                if chave in EXCECOES_REVISADAS:
                    print(f"[revisado] `{t.superficie}` — {EXCECOES_REVISADAS[chave]}")
                else:
                    falhas.append(f"baixo risco com palavra vedada não negada `{t.superficie}` (≈ {vedadas[t.radical]}): {l['frase'][:60]}")
    alto_casa = sum(any(c.negado_por is None and not c.localizacao_descartada
                        for c in ext.analisar(l["frase"], norm, mapa, "metodo")["casamentos"]) for l in alto)
    print(f"baixo risco: extrator e lista de vedadas aplicados às {len(baixo)} frases")
    print(f"alto risco (informativo): o extrator da Parte 1 casa ≥1 termo não negado em {alto_casa}/{len(alto)}")

    print("\n" + "=" * 78 + "\nDIVERSIDADE\n" + "=" * 78)
    n_neg = sum(1 for l in baixo if any(c.negado_por for c in ext.analisar(l["frase"], norm, mapa, "metodo")["casamentos"])
                or any(t.forma in ext.NEGADORES for t in norm.tokens(l["frase"])) and l["tipo_frase"] == "benigno-negacao")
    corpo_rad = {ext.sem_acento(norm.stemmer.stem(w)): w for w in CORPO}
    corpo_alto = {t.radical for l in alto for t in norm.tokens(l["frase"]) if t.radical in corpo_rad}
    corpo_baixo = [l for l in baixo if any(t.radical in corpo_alto for t in norm.tokens(l["frase"]))]
    compartilhadas = sorted({corpo_rad[t.radical] for l in corpo_baixo for t in norm.tokens(l["frase"]) if t.radical in corpo_alto})
    print(f"baixo risco com negação de sinal de alerta: {n_neg} (mínimo {MIN_NEGACAO_BAIXO})")
    print(f"baixo risco com palavra de corpo que também aparece no alto risco: {len(corpo_baixo)} (mínimo {MIN_CORPO_BAIXO}) — {', '.join(compartilhadas)}")
    print(f"tipos no treino: {dict(Counter(l['tipo_frase'] for l in treino))}")
    if n_neg < MIN_NEGACAO_BAIXO:
        falhas.append(f"só {n_neg} negações no baixo risco")
    if len(corpo_baixo) < MIN_CORPO_BAIXO:
        falhas.append(f"só {len(corpo_baixo)} frases de baixo risco com palavra de corpo compartilhada")

    print("\n" + "=" * 78 + "\nREDAÇÃO — LGPD, cláusula ND, repetição da Parte 1\n" + "=" * 78)
    paginas = {Path(f).name[:8]: (RAIZ / f).read_text(encoding="utf-8") for f in (T2, T3, T4)}
    maior_nd = 0
    for conj, linhas in (("treino", treino), ("desafio", desafio)):
        for l in linhas:
            f = l["frase"]
            if any(ch.isdigit() for ch in f) or ext.re.search(r"\banos\b", f):
                falhas.append(f"{conj}: dígito ou idade: {f[:60]}")
            nd = max(verif.maior_ngrama_comum(f, t) for t in paginas.values())
            maior_nd = max(maior_nd, nd)
            if nd >= verif.LIMITE_NGRAMA_ND:
                falhas.append(f"{conj}: {nd} palavras seguidas iguais à página (ND): {f[:60]}")
            if f in frases_p1:
                falhas.append(f"{conj}: repete frase da Parte 1: {f[:60]}")
    print(f"maior sequência de palavras igual a uma página-fonte: {maior_nd} (limite {verif.LIMITE_NGRAMA_ND})")

    print("\n" + "=" * 78 + "\nQUASE-DUPLICATA — cosseno TF-IDF sobre radicais de conteúdo\n" + "=" * 78)
    docs_t = [conteudo(norm, l["frase"]) for l in treino]
    docs_d = [conteudo(norm, l["frase"]) for l in desafio]
    docs_p = [conteudo(norm, f) for f in frases_p1]
    vet = TfidfVectorizer(analyzer=lambda d: d).fit(docs_t + docs_d + docs_p)
    limiar, sim_min, sim_max = limiar_quase_copia(vet, docs_t)
    print(f"calibração (frase × ela mesma sem 1 palavra, nas 80): mediana {limiar:.3f} "
          f"[mín {sim_min:.3f}, máx {sim_max:.3f}] → limiar de quase-cópia = {limiar:.3f}")
    Mt, Md, Mp = vet.transform(docs_t), vet.transform(docs_d), vet.transform(docs_p)
    S = cosine_similarity(Mt)
    pares = sorted(((S[i, j], i, j) for i in range(len(treino)) for j in range(i + 1, len(treino))), reverse=True)
    print(f"\n80 × 80 ({len(pares)} pares): 5 pares mais parecidos")
    for s, i, j in pares[:5]:
        print(f"  {s:.3f}  [{i + 2}] {treino[i]['frase'][:55]}…\n         [{j + 2}] {treino[j]['frase'][:55]}…")
    acima = [(s, i, j) for s, i, j in pares if s >= limiar]
    print(f"pares acima do limiar: {len(acima)}")
    for s, i, j in acima:
        falhas.append(f"quase-cópia no treino ({s:.3f}): linhas {i + 2} e {j + 2}")
    for nome, M, linhas in (("desafio", Md, [l["frase"] for l in desafio]), ("Parte 1", Mp, frases_p1)):
        C = cosine_similarity(M, Mt)
        k = C.max(axis=1)
        i_max = int(k.argmax())
        j_max = int(C[i_max].argmax())
        print(f"\n{nome} × treino: maior cosseno {k.max():.3f}\n  {linhas[i_max][:60]}…\n  [{j_max + 2}] {treino[j_max]['frase'][:60]}…")
        for i, s in enumerate(k):
            if s >= limiar:
                falhas.append(f"vazamento {nome}×treino ({s:.3f}): {linhas[i][:50]} ~ linha {int(C[i].argmax()) + 2}")
    C = cosine_similarity(Md, Mp)
    print(f"\ndesafio × Parte 1: maior cosseno {C.max():.3f}")
    if C.max() >= limiar:
        falhas.append(f"vazamento desafio×Parte 1 ({C.max():.3f})")

    vocab_treino = {w for d in docs_t for w in d}
    print("\ndesafio-vocabulario — palavras de conteúdo ausentes do treino:")
    for l, d in zip(desafio, docs_d):
        if l["tipo_frase"] == "desafio-vocabulario":
            sup = [t.superficie for t in norm.tokens(l["frase"]) if norm.e_conteudo(t) and t.radical not in vocab_treino]
            print(f"  {l['frase'][:55]}… → {', '.join(sup)}")

    print("\n" + "=" * 78 + "\nGÊNERO DA VOZ — coluna marcador_genero × concordância\n" + "=" * 78)
    dist = Counter()
    for conj, linhas in (("treino", treino), ("desafio", desafio)):
        for l in linhas:
            detectado, palavras = genero_da_voz(norm, l["frase"])
            if detectado != l.get("marcador_genero"):
                falhas.append(f"{conj}: marcador_genero={l.get('marcador_genero')!r}, concordância={detectado} {palavras}: {l['frase'][:55]}")
            if conj == "treino":
                dist[(l["situacao"], detectado)] += 1
    print(f"{'classe':12} {'feminino':>9} {'masculino':>10} {'neutro':>7}")
    for c in CLASSES:
        print(f"{c:12} {dist[(c, 'feminino')]:>9} {dist[(c, 'masculino')]:>10} {dist[(c, 'neutro')]:>7}")
        for g in ("feminino", "masculino"):
            if dist[(c, g)] < MIN_GENERO_POR_CLASSE:
                falhas.append(f"{c}: só {dist[(c, g)]} frases {g}s (mínimo {MIN_GENERO_POR_CLASSE})")
    pares = defaultdict(list)
    for l in desafio:
        if l.get("par_contrafactual"):
            pares[l["par_contrafactual"]].append(l)
    print(f"\npares contrafactuais no desafio: {len(pares)}")
    for pid, ls in sorted(pares.items()):
        generos = sorted(l["marcador_genero"] for l in ls)
        iguais = len(ls) == 2 and chave_sem_genero(norm, ls[0]["frase"]) == chave_sem_genero(norm, ls[1]["frase"])
        mesmo_rotulo = len({l["situacao"] for l in ls}) == 1
        ok = generos == ["feminino", "masculino"] and iguais and mesmo_rotulo
        print(f"  {pid}: {'OK' if ok else 'FALHA'} — {ls[0]['situacao']}; idênticas exceto concordância: {iguais}")
        if not ok:
            falhas.append(f"par {pid}: gêneros {generos}, idênticas={iguais}, mesmo rótulo={mesmo_rotulo}")

    print("\n" + "=" * 78 + "\nATALHO — palavras de conteúdo que só aparecem numa classe\n" + "=" * 78)
    df = defaultdict(Counter)
    exemplo = defaultdict(Counter)
    for l in treino:
        for t in {t.radical: t for t in norm.tokens(l["frase"]) if norm.e_conteudo(t)}.values():
            df[t.radical][l["situacao"]] += 1
            exemplo[t.radical][t.superficie] += 1
    exclusivas = sorted(((sum(c.values()), r, next(iter(c))) for r, c in df.items() if len(c) == 1), reverse=True)
    print(f"{'palavra':16} {'radical':10} {'classe':12} {'frases':>6}")
    for n, r, classe in exclusivas[:10]:
        print(f"{exemplo[r].most_common(1)[0][0]:16} {r:10} {classe:12} {n:>6}")
    compart = sorted(((min(c.values()), r) for r, c in df.items() if len(c) == 2), reverse=True)[:8]
    print("\nmais frequentes nas duas classes (alto/baixo): " + ", ".join(
        f"{exemplo[r].most_common(1)[0][0]} ({df[r]['alto risco']}/{df[r]['baixo risco']})" for _, r in compart))

    print("\n" + "=" * 78 + "\nFUNCIONAIS — informativo, adicionado depois do achado (não reprova)\n" + "=" * 78)
    analisador = TfidfVectorizer(lowercase=True, strip_accents="unicode").build_analyzer()  # igual ao notebook
    funcionais = {analisador(w)[0] for w in norm.stopwords if analisador(w)}
    df_f = defaultdict(Counter)
    for l in treino:
        for w in set(analisador(l["frase"])) & funcionais:
            df_f[w][l["situacao"]] += 1
    so_uma = sorted(((sum(c.values()), w, next(iter(c))) for w, c in df_f.items() if len(c) == 1), reverse=True)
    print(f"representação do classificador (minúsculas, sem acento, sem remover stopwords); "
          f"{len(so_uma)} palavras funcionais aparecem numa classe só:")
    print(f"{'palavra':10} {'classe':12} {'frases':>6}")
    for n, w, classe in so_uma[:12]:
        print(f"{w:10} {classe:12} {n:>6}")
    print("nas duas classes (alto/baixo): " + ", ".join(
        f"{w} ({df_f[w]['alto risco']}/{df_f[w]['baixo risco']})" for w in ("sem", "do", "quando", "nao") if w in df_f))

    print()
    if falhas:
        print(f"RESULTADO: {len(falhas)} falha(s):")
        for f in falhas:
            print(f"  - {f}")
        return 1
    print("RESULTADO: todas as verificações passaram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
