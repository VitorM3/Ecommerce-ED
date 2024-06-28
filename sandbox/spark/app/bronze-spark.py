from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("etl_bronze") \
    .getOrCreate()

# spark = configure_spark_with_delta_pip(builder).getOrCreate()

leading_path = "s3a://leading/orders.parquet"
bronze_path = "s3a://bronze/bronze_orders"

df = spark.read.parquet(leading_path)
df.show()
schema = df.schema

new_column_names = {
    "_c0": "id",
    "_c1": "price",
    "_c2": "payment_method",
    "_c3": "status",
    "_c4": "created_at",
    "_c5": "client_id",
    "_c6": "client_name",
    "_c7": "client_email",
    "_c8": "client_document",
    "_c9": "address_id",
    "_c10": "address_uf",
    "_c11": "address_city",
    "_c12": "address_country",
    "_c13": "category_id",
    "_c14": "category_name",
    "_c15": "seller_id",
    "_c16": "seller_name"
}

for old_name, new_name in new_column_names.items():
    df = df.withColumnRenamed(old_name, new_name)

# Escrita dos dados no formato Delta
df.write.format("delta").mode('overwrite').option("overwriteSchema", "true").save(bronze_path)

schema_str = ", ".join([f"{field.name} {field.dataType.simpleString()}" for field in df.schema])

spark.sql(f"""
CREATE TABLE budget_orders ({schema_str}) USING DELTA LOCATION 's3a://bronze/bronze_orders'
""").show()


spark.sql("""
SELECT * FROM budget_orders
""").show()

spark.sql("""
DELETE FROM budget_orders WHERE id = 'id'
""").show()