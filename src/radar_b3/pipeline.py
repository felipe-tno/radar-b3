from pathlib import Path
import pandas as pd

from radar_b3.config import carregar_configuracao
from radar_b3.ingestion.market_data import buscar_dados


def ingerir_dados():
    config = carregar_configuracao()

    dataframes = []

    # Coleta os benchmarks.
    for benchmark_id, benchmark in config["benchmarks"].items():
        ticker = benchmark["ticker"]
        dados = buscar_dados(ticker)

        if dados is None:
            print(f"Dados ausentes para benchmark {ticker}.")
            continue

        dados["tipo_ativo"] = "benchmark"
        dados["benchmark_id"] = benchmark_id
        dados["setor"] = None

        dataframes.append(dados)

    # Coleta as ações de cada setor.
    for setor, tickers in config["sectors"].items():
        for ticker in tickers:
            dados = buscar_dados(ticker)

            if dados is None:
                print(f"Dados ausentes para {ticker}.")
                continue

            dados["tipo_ativo"] = "acao"
            dados["benchmark_id"] = None
            dados["setor"] = setor

            dataframes.append(dados)

    if not dataframes:
        raise RuntimeError("Nenhum dado foi coletado.")

    df_bronze = pd.concat(dataframes, ignore_index=True)

    # Organiza as colunas para facilitar a inspeção.
    colunas_identificacao = [
        "Date",
        "ticker",
        "tipo_ativo",
        "setor",
        "benchmark_id",
    ]

    outras_colunas = [
        coluna
        for coluna in df_bronze.columns
        if coluna not in colunas_identificacao
    ]

    df_bronze = df_bronze[
        colunas_identificacao + outras_colunas
    ]

    return df_bronze


if __name__ == "__main__":
    df_bronze = ingerir_dados()
    print(df_bronze.head())
    print(df_bronze.shape)
    print(df_bronze["ticker"].nunique())
