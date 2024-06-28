from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


spark = SparkSession.builder \
    .appName("etl_silver") \
    .getOrCreate()

df = spark.read.format('delta').load("s3a://bronze/bronze_orders")
df.write.format("delta").mode('overwrite').option("overwriteSchema", "true").save("s3a://silver/silver_orders")
# Formatar Categorias

df.write.format("delta").mode('overwrite').option("overwriteSchema", "true").save("s3a://silver/categories")

# Formatar clientes
df.write.format("delta").mode('overwrite').option("overwriteSchema", "true").save("s3a://silver/clients")

# Formatar Endereço
df.write.format("delta").mode('overwrite').option("overwriteSchema", "true").save("s3a://silver/address")