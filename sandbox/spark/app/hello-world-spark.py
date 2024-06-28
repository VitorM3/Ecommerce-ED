from pyspark.sql import SparkSession

# Criação da sessão do Spark
spark = SparkSession.builder \
    .appName("PostgreSQL to Spark") \
    .config("spark.jars", "/usr/local/custom/libs/jbcpostgres.jar") \
    .getOrCreate()

# Configurações de conexão JDBC
jdbc_url = "jdbc:postgresql://<HOST>:<PORT>/<DATABASE>"
connection_properties = {
    "user": "postgres",
    "password": "pass@",
    "driver": "org.postgresql.Driver"
}

# Query que você deseja executar
query = "(SELECT * FROM VW_ORDERS_ETL) AS tmp"

# Carregar os dados do PostgreSQL
df = spark.read.jdbc(url=jdbc_url, table=query, properties=connection_properties)

# Mostrar os dados carregados
df.show()

# Realizar transformações e ações necessárias
# Exemplo: Contar o número de registros
count = df.count()
print(f"Número de registros: {count}")

df.printSchema()