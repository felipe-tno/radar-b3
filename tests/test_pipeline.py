
import pandas as pd
from unittest.mock import patch

from radar_b3.pipeline import coletar_ticker, executar_pipeline

TICKER = "PETR4.SA"


def test_pipeline_retry_conexao():
    dados_sucesso = pd.DataFrame({"Close": [35.2]})

    with (
        patch(
            "radar_b3.pipeline.buscar_dados",
            side_effect=[
                ConnectionError("Falha simulada"),
                ConnectionError("Falha simulada"),
                dados_sucesso,
            ],
        ) as mock_busca,
        patch("radar_b3.pipeline.time.sleep") as mock_sleep,
    ):
        resultado = coletar_ticker(TICKER)

    assert resultado is dados_sucesso
    assert mock_busca.call_count == 3
    assert mock_sleep.call_count == 2
    mock_sleep.assert_any_call(5)


def test_pipeline_falha_conexao(capsys):
    with patch(
        "radar_b3.pipeline.buscar_dados",
        side_effect=[
            ConnectionError("Falha simulada"),
            ConnectionError("Falha simulada"),
            ConnectionError("Falha simulada"),
        ],
    ) as mock_busca:
        resultado = coletar_ticker(TICKER)

    saida = capsys.readouterr().out

    assert resultado is None
    assert mock_busca.call_count == 3
    assert f"Falha na coleta de {TICKER} após 3 tentativas." in saida


def test_pipeline_sucesso_imediato():
    dados_sucesso = pd.DataFrame({"Close": [999.99]})

    with patch(
        "radar_b3.pipeline.buscar_dados",
        return_value=dados_sucesso,
    ) as mock_busca:
        resultado = coletar_ticker(TICKER)

    assert resultado.equals(dados_sucesso)
    assert mock_busca.call_count == 1


def test_dados_ausentes(capsys):
    with patch(
        "radar_b3.pipeline.buscar_dados",
        return_value=None,
    ) as mock_busca:
        resultado = coletar_ticker(TICKER)

    saida = capsys.readouterr().out

    assert resultado is None
    assert mock_busca.call_count == 1
    assert "Dados ausentes" in saida


def test_dataframe_vazio(capsys):
    with patch(
        "radar_b3.pipeline.buscar_dados",
        return_value=pd.DataFrame(),
    ) as mock_busca:
        resultado = coletar_ticker(TICKER)

    saida = capsys.readouterr().out

    assert resultado is None
    assert mock_busca.call_count == 1
    assert "Dados ausentes" in saida



def test_executar_pipeline_coleta_todos_os_ativos():
    config_teste = {
        "benchmarks": {
            "ibovespa": {
                "ticker": "^BVSP",
                "name": "Ibovespa",
            },
            "ivvb11": {
                "ticker": "IVVB11.SA",
                "name": "IVVB11",
            },
        },
        "sectors": {
            "bancos": ["ITUB4.SA", "BBAS3.SA"],
            "energia_eletrica": ["EGIE3.SA"],
        },
    }

    dados_simulados = pd.DataFrame({"Close": [100.0]})

    with (
        patch(
            "radar_b3.pipeline.carregar_configuracao",
            return_value=config_teste,
        ),
        patch(
            "radar_b3.pipeline.coletar_ticker",
            return_value=dados_simulados,
        ) as mock_coleta,
    ):
        dados_acoes, dados_benchmarks = executar_pipeline()

    assert mock_coleta.call_count == 5

    assert set(dados_benchmarks.keys()) == {
        "ibovespa",
        "ivvb11",
    }

    assert set(dados_acoes.keys()) == {
        "ITUB4.SA",
        "BBAS3.SA",
        "EGIE3.SA",
    }

    assert dados_acoes["ITUB4.SA"]["sector"] == "bancos"
    assert dados_acoes["EGIE3.SA"]["sector"] == "energia_eletrica"

    assert dados_benchmarks["ibovespa"] is dados_simulados
    assert dados_acoes["ITUB4.SA"]["dados"] is dados_simulados


def test_executar_pipeline_preserva_dados_ausentes():
    config_teste = {
        "benchmarks": {
            "ibovespa": {
                "ticker": "^BVSP",
                "name": "Ibovespa",
            },
        },
        "sectors": {
            "bancos": ["ITUB4.SA", "BBAS3.SA"],
        },
    }

    dados_simulados = pd.DataFrame({"Close": [100.0]})

    with (
        patch(
            "radar_b3.pipeline.carregar_configuracao",
            return_value=config_teste,
        ),
        patch(
            "radar_b3.pipeline.coletar_ticker",
            side_effect=[
                None,
                dados_simulados,
                None,
            ],
        ),
    ):
        dados_acoes, dados_benchmarks = executar_pipeline()

    assert dados_benchmarks["ibovespa"] is None
    assert dados_acoes["ITUB4.SA"]["dados"] is dados_simulados
    assert dados_acoes["BBAS3.SA"]["dados"] is None
