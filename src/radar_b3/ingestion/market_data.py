
import yfinance as yf

def buscar_dados(ticker):
    df = yf.download(
        ticker,
        period="1mo",
        interval="1d",
        auto_adjust=True
    )

    if df.empty: #Se o df estiver vazio, significa que não foi possível obter os dados do ticker
        print(f"Não foi possível obter dados para {ticker}.")
        return None

    return df #Se o df não estiver vazio, significa que foi possível obter os dados do ticker e retorna o df
