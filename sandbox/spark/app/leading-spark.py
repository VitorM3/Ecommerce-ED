import os
import json
import sys
import pyspark
from pyspark.sql import SparkSession
import pandas
import json
import boto3
from airflow.hooks.base import BaseHook
from delta import *

countOrders = sys.argv[1]
conn = BaseHook.get_connection('minio')


s3 = boto3.resource('s3',
                     endpoint_url=conn.host,
                     aws_access_key_id=conn.login,
                     aws_secret_access_key=conn.password
)
s3client = s3.meta.client 

# Verifique a versão do PySpark 
print (pyspark.__version__) 


spark = SparkSession.builder \
    .appName("etl_leading") \
    .enableHiveSupport() \
    .getOrCreate()


count = int(countOrders)
countBase = count
while(count != 0):
    print(count)
    path = "/usr/local/spark/resources/orders/order" + str(count) + ".csv"
    # Read JSON data using PySpark
    df = spark.read.option("inferSchema",True).csv(path)
    # Returns count of rows in the dataframe
    df.count() 
    mode = "append"
    if(count == countBase):
        mode = "overwrite"

    df.write.mode(mode).format("parquet").save("s3a://leading/orders.parquet")
    order_raw_data = spark.read.parquet("s3a://leading/orders.parquet")
    order_raw_data.count()

    if(count == 1):
        spark.sql("""
DROP TABLE IF EXISTS leading_orders
""")
        spark.sql("""
CREATE EXTERNAL TABLE leading_orders (
    id BIGINT,
    price DOUBLE,
    status STRING,
    payment_method STRING,
    client_id BIGINT,
    client_name STRING,
    client_email STRING,
    client_document STRING,
    address_id BIGINT,
    address_uf STRING,
    address_country STRING,
    category_id BIGINT,
    category_name STRING,
    seller_id BIGINT,
    seller_name STRING
)
STORED AS PARQUET
LOCATION 's3a://leading/orders.parquet';
""").show()

    os.remove(path)
    count -= 1