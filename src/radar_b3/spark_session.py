from pyspark.sql import SparkSession


def criar_spark_session():
    spark = (
        SparkSession.builder
        .appName("RadarB3")
        .master("local[*]")
        .getOrCreate()
    )

    return spark
