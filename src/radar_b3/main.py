from radar_b3.pipeline import ingerir_dados
from radar_b3.spark_session import criar_spark_session
from radar_b3.transformations.prices import transformar_precos


# 1. Ingestão: gera o Bronze em pandas.
df_bronze = ingerir_dados()

# 2. Inicialização do Spark.
spark = criar_spark_session()

# 3. Conversão de pandas para PySpark.
df_bronze_spark = spark.createDataFrame(df_bronze)

# 4. Inspeção do DataFrame Spark.
df_bronze_spark.printSchema()
df_bronze_spark.show(5)

# 5. Ponto de entrada para as transformações Silver.
df_silver = transformar_precos(df_bronze_spark)

spark.stop()
