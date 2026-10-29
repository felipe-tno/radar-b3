from radar_b3.config import carregar_configuracao


def test_carregar_configuracao():
    config = carregar_configuracao()

    assert config["benchmarks"]["ibovespa"]["ticker"] == "^BVSP"
    assert config["benchmarks"]["ivvb11"]["ticker"] == "IVVB11.SA"
    assert "bancos" in config["sectors"]
    assert "ITUB4.SA" in config["sectors"]["bancos"]
