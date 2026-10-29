from radar_b3.ingestion.market_data import buscar_dados
import time


def executar_pipeline(ticker):
    for tentativa in range(3):
        try:
            dados = buscar_dados(ticker)

            
            if dados is None:
                print(f"Dados ausentes.")
                return


            print(f"Dados obtidos para {ticker}")
            print(dados.head())
            return


        except Exception as erro:
            print(f"Falha na coleta de {ticker}, {erro}, Tentativa {tentativa + 1}")

            if tentativa < 2:
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)

    print(f"Falha na coleta de {ticker} após 3 tentativas. Certifique-se que o ticker existe e que você está conectado à internet.")




if __name__ == "__main__":
    executar_pipeline("PETR4.SA")