import pandas as pd
from unittest.mock import patch
from radar_b3.pipeline import executar_pipeline

TICKER = 'PETR4.SA'
#Conexão caiu de primeira mas na segunda tentativa já volta a funcionar
def test_pipeline_retry_conexao():
    with (
        patch(
            "radar_b3.pipeline.buscar_dados",
            side_effect=[
                ConnectionError("Falha simulada"),
                ConnectionError("Falha simulada"),
                pd.DataFrame({"Close": [35.2]}),
            ],
        ) as mock_busca,
        patch("radar_b3.pipeline.time.sleep") as mock_sleep,
    ):
        executar_pipeline(TICKER)

    assert mock_busca.call_count == 3
    assert mock_sleep.call_count == 2
    mock_sleep.assert_any_call(5)

#Conexão caiu de todas as tentativas
def test_pipeline_falha_conexao(capsys):
    with patch(
        "radar_b3.pipeline.buscar_dados",
        side_effect=[
            ConnectionError("Falha simulada"),
            ConnectionError("Falha simulada"),
            ConnectionError("Falha simulada"),
        ],
    ) as mock_busca:
        executar_pipeline(TICKER)

    saida = capsys.readouterr().out
    assert mock_busca.call_count == 3
    assert f"Falha na coleta de {TICKER} após 3 tentativas." in saida

#Sucesso imediato
def test_pipeline_sucesso_imediato(capsys):
    dados_sucesso = pd.DataFrame ({"Close": [35.2, 36.1]})
    with patch(
        "radar_b3.pipeline.buscar_dados",
        side_effect=[
            dados_sucesso
        ],
    ) as mock_busca:
        executar_pipeline(TICKER)

    saida = capsys.readouterr().out
    assert mock_busca.call_count == 1
    assert f"Dados obtidos para {TICKER}" in saida

#Dados ausentes
def test_dados_ausentes(capsys):
    with patch(
        "radar_b3.pipeline.buscar_dados",
        return_value=None,
    ) as mock_busca:
        executar_pipeline(TICKER)

    saida = capsys.readouterr().out
    assert mock_busca.call_count == 1
    assert f"Dados ausentes." in saida

