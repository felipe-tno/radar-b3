import pandas as pd
from radar_b3.pipeline import executar_pipeline

def calcular_retorno(df, periodo="6mo"):
    if df is None or df.empty:
        return None

    periodos = {
        "1d": pd.DateOffset(days=1),
        "1w": pd.DateOffset(days=7),
        "30d": pd.DateOffset(days=30),
        "6mo": pd.DateOffset(days=180),
    }

    if periodo not in periodos:
        raise ValueError(
            f"Período inválido: {periodo}"
            f"Use um desses períodos: {list(periodos)}"
        )

    if "Close" not in df.columns:
        return None

    print("Colunas:", df.columns)
    print("Tipo de df['Close']:", type(df["Close"]))

    precos = df["Close"].dropna().sort_index()

    if precos.empty:
        return None

#Ultimo preço disponível
    data_final = precos.index[-1]
    preco_final = precos.iloc[-1]

#Inicio do período
    data_alvo = data_final - periodos[periodo]

#Último fechamento disponível na data alvo ou antes dela
    precos_anteriores = precos.loc[precos.index <= data_alvo]
    
    if precos_anteriores.empty:
        return None

    
    preco_inicial = precos_anteriores.iloc[-1]

    if preco_inicial <= 0 or preco_final < 0:
        return None

    retorno = (preco_final / preco_inicial - 1) * 100

    return retorno




def calcular_retorno_por_periodo(dados_acoes, dados_benchmark, periodo):
    retornos_acoes = {}
    retornos_benchmarks = {}

    for ticker,info in dados_acoes.items():
        retornos_acoes[ticker] = {
            "sector": info["sector"],
            "retorno": calcular_retorno(info["dados"],periodo),
        }

    for benchmark_id, dados in dados_benchmarks.items():
        retornos_benchmarks[benchmark_id] = calcular_retorno(dados,periodo)

        return retornos_acoes, retornos_benchmarks


dados_acoes, dados_benchmarks = executar_pipeline()

retornos_acoes, retornos_benchmarks = calcular_retorno_por_periodo(
    dados_acoes,
    dados_benchmarks,
    periodo="30d",
)