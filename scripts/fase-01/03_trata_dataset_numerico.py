"""Tratamento do dataset UCI Heart Disease (Cleveland, id=45) — Fase 1.

Le document/datasets/raw/heart-disease-raw.csv (gerado por
01_coleta_dataset_numerico.py) e grava a versao processada em
document/datasets/processed/ (.csv e .xlsx). As decisoes abaixo foram
tomadas em conversa com o time e sao reaproveitadas em
document/datasets/dicionario-de-dados.md e em
document/fase-01/governanca-e-vies.md — nao mudar sem atualizar os dois.

DECISAO 1 — ausencias em ca e thal: NAO IMPUTAR (fica NaN/celula vazia).
  (a) Imputar pela moda do dataset inteiro, antes do split treino/teste da
      Fase 2, e VAZAMENTO DE DADOS — a imputacao (quando fizer sentido) tem
      que acontecer dentro do fold de validacao, e isso e responsabilidade
      da Fase 2, nao desta fase de coleta.
  (b) ca (numero de vasos por fluoroscopia) e thal (cintilografia com talio)
      sao exames invasivos/caros. A ausencia provavelmente NAO e aleatoria
      (MNAR — missing not at random: paciente com quadro menos grave pode
      nunca ter sido submetido ao exame). Imputar pela moda apagaria esse
      sinal. Impacto: 6 linhas em 303 (~2%) tem alguma ausencia.

DECISAO 2 — alvo: manter as DUAS colunas.
  `num` e a coluna ORIGINAL da UCI (0 a 4, severidade) e NAO e renomeada.
  `alvo_binario` e derivada (0 se num==0, 1 se num>0). A Fase 2 usa o
  binario para classificacao de risco (54,1% / 45,9%, bem balanceado); a
  Fase 6 pode querer a severidade original para previsao de crise.

DECISAO 3 — faixas de plausibilidade sao SANIDADE DE DADO, nao referencia
  clinica. Servem para pegar erro de digitacao/sensor, nao para diagnostico.
  Nenhuma linha e removida por cair fora da faixa — o script so REPORTA.
  A checagem cruzada de thalach contra 220-idade e um AVISO, nao rejeicao:
  220-idade e estimativa populacional com desvio de ~10-12 bpm, entao
  rejeitar por ela descartaria dado real (a base tem alguns casos legitimos
  acima da estimativa, o que o relatorio abaixo evidencia).
  Na execucao real sobre esta base, 10 linhas disparam esse aviso — e os 10
  sao BENIGNOS, nao erro de dado: thalach e a FC maxima atingida em teste de
  esforco, e um individuo bem condicionado ultrapassa a estimativa
  populacional com naturalidade. O maior excesso sobre o limiar (ja com a
  margem de 15 bpm somada) e de 14 bpm, no indice 188 (idade=54,
  thalach=195, limiar=181). Nenhum caso chega perto de um valor
  fisiologicamente impossivel (a faixa absoluta [60,220] continua intacta
  em todas as linhas). Ninguem deve ler "10 avisos" como problema de
  qualidade do dado.

ALERTA (nao aplicavel aqui, mas registrado para o futuro): nas outras bases
  do UCI Heart Disease (Hungria, Suica, VA Long Beach) valores 0 em `chol` e
  `trestbps` sao SENTINELA DE AUSENCIA, nao medida real. Na Cleveland isso
  nao ocorre (minimos observados: chol=126, trestbps=94), mas se o grupo
  agregar as outras bases numa fase futura, tratar 0 como medida real vai
  ser um bug silencioso. Por isso o script abaixo avisa (nao falha, nao
  remove) se encontrar 0 nessas colunas — para nunca passar despercebido.

ACHADO DE VIES A PRESERVAR (ver 6. CRUZAMENTO ALVO x SEXO abaixo): a base e
  68% masculina e a prevalencia do alvo binario e de 25,8% em sex=0 (mulher)
  contra 55,3% em sex=1 (homem). Alem da epidemiologia real (doenca
  coronariana e de fato mais prevalente e mais precoce em homens), a
  Cleveland e uma base de pacientes ENCAMINHADOS PARA ANGIOGRAFIA, e
  mulheres com dor toracica sao historicamente menos encaminhadas para
  investigacao invasiva — vies de encaminhamento, nao so epidemiologia.
  Consequencia pratica: um modelo treinado aqui tende a SUBDETECTAR em
  mulheres, que e o lado mais perigoso do erro numa triagem cardiologica.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# Nao ha nenhuma operacao aleatoria neste script (renomeio, derivacao e
# validacao sao deterministicos) — por isso nao ha semente para fixar aqui.

RAW_CSV_PATH = (
    Path(__file__).resolve().parents[2]
    / "document"
    / "datasets"
    / "raw"
    / "heart-disease-raw.csv"
)
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "document" / "datasets" / "processed"
PROCESSED_CSV_PATH = PROCESSED_DIR / "heart-disease-processed.csv"
PROCESSED_XLSX_PATH = PROCESSED_DIR / "heart-disease-processed.xlsx"

# Nome novo (pt-BR) -> nome original UCI. `num` fica de fora de proposito —
# e mantido com o nome original por decisao explicita (ver DECISAO 2 acima).
MAPA_RENOMEIO = {
    "age": "idade",
    "sex": "sexo",
    "cp": "tipo_dor_peito",
    "trestbps": "pressao_arterial_repouso",
    "chol": "colesterol_serico",
    "fbs": "glicemia_jejum_alta",
    "restecg": "eletrocardiograma_repouso",
    "thalach": "frequencia_cardiaca_maxima",
    "exang": "angina_induzida_exercicio",
    "oldpeak": "depressao_st_exercicio",
    "slope": "inclinacao_st_exercicio",
    "ca": "numero_vasos_fluoroscopia",
    "thal": "talassemia",
}

# Faixas de SANIDADE DE DADO (nao clinicas) — ver DECISAO 3.
FAIXAS_PLAUSIBILIDADE = {
    "idade": (18, 100),
    "pressao_arterial_repouso": (60, 250),
    "colesterol_serico": (100, 600),
    "frequencia_cardiaca_maxima": (60, 220),
}
MARGEM_FC_MAXIMA_ESTIMADA = 15  # bpm, acima de (220 - idade) — ver DECISAO 3

LIMITES_FAIXAS_ETARIAS = [0, 39, 49, 59, 69, 200]
ROTULOS_FAIXAS_ETARIAS = ["<40", "40-49", "50-59", "60-69", "70+"]


def carregar_dado_cru() -> pd.DataFrame:
    if not RAW_CSV_PATH.exists():
        raise FileNotFoundError(
            f"{RAW_CSV_PATH} nao existe. Rode 01_coleta_dataset_numerico.py primeiro."
        )
    return pd.read_csv(RAW_CSV_PATH)


def renomear_colunas(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=MAPA_RENOMEIO)


def criar_alvo_binario(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["alvo_binario"] = (df["num"] > 0).astype(int)
    return df


def checar_sentinela_zero(df: pd.DataFrame) -> None:
    print("=" * 78)
    print("CHECAGEM DE SENTINELA DE AUSENCIA (0 em chol/trestbps)")
    print("=" * 78)
    for coluna in ["colesterol_serico", "pressao_arterial_repouso"]:
        n_zeros = int((df[coluna] == 0).sum())
        if n_zeros > 0:
            print(
                f"[AVISO] {coluna} tem {n_zeros} valor(es) igual a 0. Em outras bases "
                "do UCI Heart Disease (Hungria/Suica/VA Long Beach) 0 e sentinela de "
                "ausencia, nao medida real. Confirmar antes de tratar como dado valido."
            )
        else:
            print(f"- {coluna}: nenhum valor 0 encontrado (esperado para Cleveland).")
    print()


def reportar_plausibilidade(df: pd.DataFrame) -> None:
    print("=" * 78)
    print("VALIDACAO DE PLAUSIBILIDADE (sanidade de dado, NAO referencia clinica)")
    print("Regra geral: nenhuma linha e removida. So relatorio.")
    print("=" * 78)
    for coluna, (minimo, maximo) in FAIXAS_PLAUSIBILIDADE.items():
        fora_da_faixa = df[(df[coluna] < minimo) | (df[coluna] > maximo)]
        print(f"- {coluna}: faixa aceita [{minimo}, {maximo}]  ->  {len(fora_da_faixa)} linha(s) fora")
        for indice, valor in fora_da_faixa[coluna].items():
            print(f"    [AVISO] indice {indice}: {coluna}={valor} fora da faixa de sanidade")

    print(
        "- checagem cruzada frequencia_cardiaca_maxima vs (220 - idade + "
        f"{MARGEM_FC_MAXIMA_ESTIMADA}): aviso, nao rejeicao (220-idade e estimativa "
        "populacional com desvio de ~10-12 bpm)"
    )
    limite_fc = 220 - df["idade"] + MARGEM_FC_MAXIMA_ESTIMADA
    excede_fc = df[df["frequencia_cardiaca_maxima"] > limite_fc]
    print(f"    {len(excede_fc)} linha(s) excedem a estimativa com margem")
    excesso_maximo = 0.0
    indice_excesso_maximo = None
    for indice, linha in excede_fc.iterrows():
        limiar_linha = 220 - linha["idade"] + MARGEM_FC_MAXIMA_ESTIMADA
        excesso = linha["frequencia_cardiaca_maxima"] - limiar_linha
        if excesso > excesso_maximo:
            excesso_maximo = excesso
            indice_excesso_maximo = indice
        print(
            f"    [AVISO] indice {indice}: idade={linha['idade']} "
            f"frequencia_cardiaca_maxima={linha['frequencia_cardiaca_maxima']} "
            f"(estimativa+margem={limiar_linha}, excesso={excesso})"
        )
    if len(excede_fc) > 0:
        print(
            f"    [BENIGNO] os {len(excede_fc)} avisos acima NAO sao erro de dado: "
            "thalach e a FC maxima atingida em esforco, e um individuo bem "
            "condicionado ultrapassa a estimativa populacional com naturalidade. "
            f"Maior excesso sobre o limiar (ja com margem): {excesso_maximo} bpm, "
            f"no indice {indice_excesso_maximo}. Nenhuma linha viola a faixa "
            "absoluta de sanidade [60, 220]. Nao ler isto como problema de "
            "qualidade do dado."
        )
    print()


def imprimir_relatorio_final(df: pd.DataFrame) -> None:
    print("=" * 78)
    print("RELATORIO FINAL DO DATASET PROCESSADO")
    print("=" * 78)
    n_linhas, n_colunas = df.shape
    print(f"Linhas: {n_linhas}")
    print(f"Colunas: {n_colunas}")
    print()

    print("-- nulos por coluna --")
    for coluna in df.columns:
        n_nulos = int(df[coluna].isna().sum())
        if n_nulos > 0:
            pct = 100 * n_nulos / n_linhas
            print(f"  {coluna}: {n_nulos} ({pct:.1f}%)")
    print()

    print("-- distribuicao do alvo original (num, 0 a 4) --")
    contagem = df["num"].value_counts().sort_index()
    percentual = df["num"].value_counts(normalize=True).sort_index() * 100
    for nivel in contagem.index:
        print(f"  num={nivel}: {contagem[nivel]:>4}  ({percentual[nivel]:5.1f}%)")

    print("-- distribuicao do alvo_binario (derivado) --")
    contagem_bin = df["alvo_binario"].value_counts().sort_index()
    percentual_bin = df["alvo_binario"].value_counts(normalize=True).sort_index() * 100
    for nivel in contagem_bin.index:
        print(
            f"  alvo_binario={nivel}: {contagem_bin[nivel]:>4}  ({percentual_bin[nivel]:5.1f}%)"
        )
    print()

    print("-- distribuicao por sexo (0=feminino, 1=masculino) --")
    contagem_sexo = df["sexo"].value_counts().sort_index()
    percentual_sexo = df["sexo"].value_counts(normalize=True).sort_index() * 100
    for valor in contagem_sexo.index:
        print(f"  sexo={valor}: {contagem_sexo[valor]:>4}  ({percentual_sexo[valor]:5.1f}%)")

    print("-- distribuicao por faixa etaria (bins so deste relatorio) --")
    faixa = pd.cut(df["idade"], bins=LIMITES_FAIXAS_ETARIAS, labels=ROTULOS_FAIXAS_ETARIAS)
    contagem_faixa = faixa.value_counts().sort_index()
    percentual_faixa = faixa.value_counts(normalize=True).sort_index() * 100
    for rotulo in contagem_faixa.index:
        print(
            f"  {rotulo:<6}: {contagem_faixa[rotulo]:>4}  ({percentual_faixa[rotulo]:5.1f}%)"
        )
    print()

    print("-- CRUZAMENTO alvo_binario x sexo (achado de vies a preservar) --")
    tabela_contagem = pd.crosstab(
        df["sexo"], df["alvo_binario"], margins=True, margins_name="total"
    )
    tabela_percentual_linha = pd.crosstab(df["sexo"], df["alvo_binario"], normalize="index") * 100
    print("Contagem (linhas=sexo, colunas=alvo_binario, 0=ausencia 1=presenca):")
    print(tabela_contagem.to_string())
    print()
    print("Percentual dentro de cada sexo:")
    print(tabela_percentual_linha.round(1).to_string())
    print(
        "\n[REGISTRAR EM governanca-e-vies.md] prevalencia de alvo_binario=1 e "
        f"{tabela_percentual_linha.loc[0, 1]:.1f}% em sexo=0 (feminino) contra "
        f"{tabela_percentual_linha.loc[1, 1]:.1f}% em sexo=1 (masculino), numa base "
        f"{percentual_sexo[1]:.0f}% masculina — epidemiologia real + provavel vies de "
        "encaminhamento (mulheres com dor toracica historicamente menos encaminhadas "
        "para angiografia). Risco: modelo treinado aqui tende a subdetectar em mulheres."
    )
    print()


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = carregar_dado_cru()
    df = renomear_colunas(df)
    df = criar_alvo_binario(df)

    checar_sentinela_zero(df)
    reportar_plausibilidade(df)

    # index=False e os NaN nativos do pandas viram celula vazia no csv/xlsx
    # (nao a string "NaN", nao sentinela -9) — exigencia da DECISAO 1.
    df.to_csv(PROCESSED_CSV_PATH, index=False)
    df.to_excel(PROCESSED_XLSX_PATH, index=False)
    print(f"[OK] Dataset processado salvo em {PROCESSED_CSV_PATH}")
    print(f"[OK] Dataset processado salvo em {PROCESSED_XLSX_PATH}")
    print()

    imprimir_relatorio_final(df)


if __name__ == "__main__":
    main()
