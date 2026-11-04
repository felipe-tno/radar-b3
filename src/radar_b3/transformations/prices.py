from pyspark.sql.functions import col, sum

def transformar_precos(df_bronze_spark):
    
    return df_bronze_spark


from pyspark.sql.functions import col, sum


def validar_qualidade_precos(df):
    problemas = []

    # High menor que Low
    df_errohl = df.filter(col("High") < col("Low"))
    if df_errohl.count() > 0:
        problemas.append("Erro na qualidade dos dados. HL")

    # Close fora do intervalo High-Low
    df_errocl = df.filter(
        (col("Close") > col("High")) |
        (col("Close") < col("Low"))
    )
    if df_errocl.count() > 0:
        problemas.append("Erro na qualidade dos dados. Close")

    # Duplicidades por ativo e data
    df_duplicatas = (
        df.groupBy("Date", "ticker")
        .count()
        .filter("count > 1")
    )
    if df_duplicatas.count() > 0:
        problemas.append("Erro de duplicatas")

    # Valores nulos nos preços
    df_nulos = df.select(
        sum(col("Open").isNull().cast("int")).alias("Open_nulos"),
        sum(col("High").isNull().cast("int")).alias("High_nulos"),
        sum(col("Low").isNull().cast("int")).alias("Low_nulos"),
        sum(col("Close").isNull().cast("int")).alias("Close_nulos")
    )

    resultado_nulos = df_nulos.collect()[0].asDict()

    if any(valor > 0 for valor in resultado_nulos.values()):
        problemas.append("Erro. Dados Nulos")

    return problemas

