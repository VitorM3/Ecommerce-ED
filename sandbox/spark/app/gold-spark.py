from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql import functions as F
import psycopg2
from pyspark.sql.types import TimestampType

spark = SparkSession.builder \
    .appName("etl_gold") \
    .getOrCreate()

postgres_url = "jdbc:postgresql://database_dimensional:5432/postgres"
postgres_properties = {
    "user": "postgres",
    "password": "pass@",
    "driver": "org.postgresql.Driver"
}

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="pass@",
    host="database_dimensional",
    port="5432"
)
cursor = conn.cursor()

orders = spark.read.format('delta').load("s3a://silver/silver_orders")
categories = spark.read.format('delta').load("s3a://silver/categories")
clients = spark.read.format('delta').load("s3a://silver/clients")
address = spark.read.format('delta').load("s3a://silver/address")

def delete_from_postgres(sql_stmt):
    try:
        # Estabelece a conexão e executa a instrução
        conn = spark.read.jdbc(url=postgres_url, table="(SELECT  FROM)", properties=postgres_properties)
        conn.execute(sql_stmt)
        print("Dados deletados com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar dados: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()
        
delete_from_postgres("DELETE FROM fact_order")


dim_address = address.select("address_id", "address_uf", "address_city","address_country")
dim_address = dim_address.withColumn("address_id", col("address_id").cast("integer"))
new_column_names_address = {
    "address_id": "address_id",
    "address_uf": "uf",
    "address_city": "city",
    "address_country": "country",
}
for old_name, new_name in new_column_names_address.items():
    dim_address = dim_address.withColumnRenamed(old_name, new_name)
dim_address_duplicated = dim_address.dropDuplicates(["address_id"])

dim_address_duplicated.write.jdbc(url=postgres_url, table="temp_address", mode="overwrite", properties=postgres_properties)

merge_sql = """
INSERT INTO dim_address AS tgt
SELECT * FROM temp_address AS src
ON CONFLICT (address_id)
DO UPDATE SET
uf = EXCLUDED.uf,
city = EXCLUDED.country
"""

cursor.execute(merge_sql)
conn.commit()

cursor.execute('DROP TABLE temp_address')
conn.commit()



dim_product_category = categories.select("category_id", "category_name")
dim_product_category = dim_product_category.withColumn("category_id", col("category_id").cast("integer"))

new_column_names_category = {
    "category_id": "category_id",
    "category_name": "name",
}

for old_name, new_name in new_column_names_category.items():
    dim_product_category = dim_product_category.withColumnRenamed(old_name, new_name)

dim_category_duplicated = dim_product_category.dropDuplicates(["category_id"])

dim_category_duplicated.write.jdbc(url=postgres_url, table="temp_category", mode="overwrite", properties=postgres_properties)

merge_sql = """
INSERT INTO dim_product_category AS tgt
SELECT * FROM temp_category AS src
ON CONFLICT (category_id)
DO UPDATE SET
name = EXCLUDED.name
"""

cursor.execute(merge_sql)
conn.commit()

cursor.execute('DROP TABLE temp_category')
conn.commit()



dim_client = categories.select("client_id", "client_name","client_email","client_document")

new_column_names_client = {
    "client_id": "client_id",
    "client_name": "name",
}

for old_name, new_name in new_column_names_client.items():
    dim_client = dim_client.withColumnRenamed(old_name, new_name)


dim_client = dim_client.withColumn("client_id", col("client_id").cast("integer"))
dim_client_duplicated = dim_client.dropDuplicates(["client_id"])

dim_client_duplicated.write.jdbc(url=postgres_url, table="temp_client", mode="overwrite", properties=postgres_properties)

merge_sql = """
INSERT INTO dim_client AS tgt
SELECT * FROM temp_client AS src
ON CONFLICT (client_id)
DO UPDATE SET
name = EXCLUDED.name
"""

cursor.execute(merge_sql)
conn.commit()

cursor.execute('DROP TABLE temp_client')
conn.commit()



dim_seller = orders.select("seller_id","seller_name")
dim_seller = dim_seller.withColumn("seller_id", col("seller_id").cast("integer"))
new_column_names_seller = {
    "seller_id": "seller_id",
    "name": "seller_name"
}
for old_name, new_name in new_column_names_seller.items():
    dim_seller = dim_seller.withColumnRenamed(old_name, new_name)
dim_seller_duplicated = dim_seller.dropDuplicates(["seller_id"])

dim_seller_duplicated.write.jdbc(url=postgres_url, table="temp_seller", mode="overwrite", properties=postgres_properties)

merge_sql = """
INSERT INTO dim_seller AS tgt
SELECT * FROM temp_seller AS src
ON CONFLICT (seller_id)
DO UPDATE SET
name = EXCLUDED.name
"""

cursor.execute(merge_sql)
conn.commit()

cursor.execute('DROP TABLE temp_seller')
conn.commit()


fact_order = orders.select("client_id","address_id", "category_id", "seller_id","id","price","payment_method","status","created_at")
new_column_names = {
    "client_id": "dim_client_id",
    "address_id": "dim_address_id",
    "category_id": "dim_category_product_id",
    "id": "order_id",
    "seller_id": "dim_seller_id",
    "price": "price",
    "payment_method": "payment_method",
    "status": "status",
    "created_at": "created_at",
}

for old_name, new_name in new_column_names.items():
    fact_order = fact_order.withColumnRenamed(old_name, new_name)


fact_order = fact_order.withColumn("dim_client_id", col("dim_client_id").cast("integer"))
fact_order = fact_order.withColumn("dim_address_id", col("dim_address_id").cast("integer"))
fact_order = fact_order.withColumn("dim_category_product_id", col("dim_category_product_id").cast("integer"))
fact_order = fact_order.withColumn("order_id", col("order_id").cast("integer"))
fact_order = fact_order.withColumn("dim_seller_id", col("dim_seller_id").cast("integer"))
fact_order = fact_order.withColumn("price", col("price").cast("float"))
fact_order = fact_order.withColumn("created_at", col("created_at").cast(TimestampType()))
fact_order = fact_order.dropDuplicates(["dim_client_id","dim_address_id","dim_category_product_id","order_id"])
fact_order.write.jdbc(url=postgres_url, table="temp_order", mode="overwrite", properties=postgres_properties)

merge_sql = """
INSERT INTO fact_order AS tgt
SELECT * FROM temp_order AS src
ON CONFLICT (dim_client_id,dim_address_id,dim_category_product_id,dim_seller_id,order_id)
DO UPDATE SET
price = EXCLUDED.price,
payment_method = EXCLUDED.payment_method,
status = EXCLUDED.status,
created_at = EXCLUDED.created_at
"""

cursor.execute(merge_sql)
conn.commit()

cursor.execute('DROP TABLE temp_order')
conn.commit()
# Fechar a conexão
cursor.close()
conn.close()