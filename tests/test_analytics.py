import pandas as pd
import pytest

from radar_b3.analytics.peformance import calcular_retorno


def criar_df(precos, datas):
    return pd.DataFrame(
        {"Close": precos},
        index=pd.to_datetime(datas),
    )


def test_retorno_positivo():
    df = criar_df(
        [30.0, 36.0],
        ["2026-04-20", "2026-10-26"],
    )
    assert calcular_retorno(df) == pytest.approx(20.0)


def test_retorno_negativo():
    df = criar_df(
        [40.0, 30.0],
        ["2026-04-20", "2026-10-26"],
    )
    assert calcular_retorno(df) == pytest.approx(-25.0)


def test_retorno_zero():
    df = criar_df(
        [30.0, 30.0],
        ["2026-04-20", "2026-10-26"],
    )
    assert calcular_retorno(df) == pytest.approx(0.0)


def test_dataframe_ausente():
    assert calcular_retorno(None) is None


def test_dataframe_vazio():
    df = criar_df([], [])
    assert calcular_retorno(df) is None


def test_todos_os_precos_ausentes():
    df = criar_df(
        [None, None],
        ["2026-10-23", "2026-10-26"],
    )
    assert calcular_retorno(df) is None


def test_preco_inicial_zero():
    df = criar_df(
        [0.0, 36.0],
        ["2026-04-20", "2026-10-26"],
    )
    assert calcular_retorno(df) is None


def test_preco_final_negativo():
    df = criar_df(
        [30.0, -1.0],
        ["2026-04-20", "2026-10-26"],
    )
    assert calcular_retorno(df) is None


def test_periodo_1d():
    df = criar_df(
        [100.0, 110.0, 120.0],
        ["2026-10-22", "2026-10-23", "2026-10-26"],
    )
    assert calcular_retorno(df, "1d") == pytest.approx(
        (120 / 110 - 1) * 100
    )


def test_periodo_sem_historico_suficiente():
    df = criar_df(
        [100.0, 110.0],
        ["2026-10-20", "2026-10-26"],
    )
    assert calcular_retorno(df, "30d") is None


def test_periodo_invalida():
    df = criar_df(
        [100.0, 110.0],
        ["2026-10-23", "2026-10-26"],
    )
    with pytest.raises(ValueError):
        calcular_retorno(df, "90d")
