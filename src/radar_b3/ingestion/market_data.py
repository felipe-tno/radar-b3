import pandas as pd
import yfinance as yf


def buscar_dados(ticker):
    df = yf.download(
        ticker,
        period="7mo",
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    if df.empty:
        return None

    # O yfinance pode retornar colunas MultiIndex.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # A data passa a ser uma coluna explícita.
    df = df.reset_index()

    # Identifica o ativo de origem.
    df["ticker"] = ticker

    df.columns.name = None
    return df
