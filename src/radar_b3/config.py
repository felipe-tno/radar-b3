from pathlib import Path
from radar_b3.ingestion.market_data import buscar_dados

import yaml

def carregar_configuracao():
    raiz_projeto = Path(__file__).resolve().parents[2]
    caminho_config = raiz_projeto / "config" / "assets.yaml"

    with caminho_config.open("r", encoding="utf-8") as arquivo:
        configuracao = yaml.safe_load(arquivo)

    return configuracao
