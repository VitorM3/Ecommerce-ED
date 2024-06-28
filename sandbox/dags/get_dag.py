from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.hooks.base import BaseHook


minio = BaseHook.get_connection('minio')



def get_data():
    pg_hook = PostgresHook.get_hook('postgres_database_base')
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute("select COUNT(1) from vw_orders_etl")
    countData = cursor.fetchall()
    count = int(countData[0][0])
    countDataValue = 0
    countName = 1
    while(countDataValue != count):
        pg_hook.copy_expert("COPY (SELECT * FROM VW_ORDERS_ETL LIMIT 1000 offset " +  str(countDataValue) + ") TO STDOUT WITH CSV HEADER", filename="/usr/local/spark/resources/orders/order" + str(countName) + ".csv")
        countDataValue += 1000
        countName += 1

args = {
    'owner': 'Airflow',
}

with DAG(
    dag_id='etl',
    default_args=args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['ETL'],
) as dag:

    get_data_dag = PythonOperator(
    task_id='etl_get_data',
    provide_context=True,
    python_callable=get_data,
    dag=dag,
    )

    leading_dag = SparkSubmitOperator(
        task_id="etl_leading",
        application="/usr/local/spark/app/leading-spark.py",
        name='ETL Spark Leading',
        conn_id="spark_default",
        verbose=1,
        application_args=[str(25)],
        conf={
            "spark.master":'spark://spark:7077',
            "spark.hadoop.fs.s3a.endpoint": minio.host,
            "spark.hadoop.fs.s3a.access.key": minio.login,
            "spark.hadoop.fs.s3a.secret.key": minio.password,
            "spark.hadoop.fs.s3a.path.style.access": 'true',
            "spark.driver.memory": "5g",
            "spark.executor.memory": "3g",
            "spark.yarn.am.memory": "1g",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem"
            },
        packages="org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262",
        dag=dag
    )

    bronze_dag = SparkSubmitOperator(
        task_id="etl_bronze",
        application="/usr/local/spark/app/bronze-spark.py",
        name='ETL Spark Bronze',
        conn_id="spark_default",
        verbose=1,
        conf={
            "spark.master":'spark://spark:7077',
            "spark.hadoop.fs.s3a.endpoint": minio.host,
            "spark.hadoop.fs.s3a.access.key": minio.login,
            "spark.hadoop.fs.s3a.secret.key": minio.password,
            "spark.hadoop.fs.s3a.path.style.access": 'true',
            "spark.driver.memory": "5g",
            "spark.executor.memory": "3g",
            "spark.yarn.am.memory": "1g",
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem"
            },
        packages="org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,io.delta:delta-spark_2.12:3.2.0",
        dag=dag
    )

    silver_dag = SparkSubmitOperator(
        task_id="etl_silver",
        application="/usr/local/spark/app/silver-spark.py",
        name='ETL Spark Silver',
        conn_id="spark_default",
        verbose=1,
        conf={
            "spark.master":'spark://spark:7077',
            "spark.hadoop.fs.s3a.endpoint": minio.host,
            "spark.hadoop.fs.s3a.access.key": minio.login,
            "spark.hadoop.fs.s3a.secret.key": minio.password,
            "spark.hadoop.fs.s3a.path.style.access": 'true',
            "spark.driver.memory": "5g",
            "spark.executor.memory": "3g",
            "spark.yarn.am.memory": "1g",
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem"
            },
        packages="org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,io.delta:delta-spark_2.12:3.2.0",
        dag=dag
    )

    gold_dag = SparkSubmitOperator(
        task_id="etl_gold",
        application="/usr/local/spark/app/gold-spark.py",
        name='ETL Spark Gold',
        conn_id="spark_default",
        verbose=1,
        conf={
            "spark.master":'spark://spark:7077',
            "spark.hadoop.fs.s3a.endpoint": minio.host,
            "spark.hadoop.fs.s3a.access.key": minio.login,
            "spark.hadoop.fs.s3a.secret.key": minio.password,
            "spark.hadoop.fs.s3a.path.style.access": 'true',
            "spark.driver.memory": "5g",
            "spark.executor.memory": "3g",
            "spark.yarn.am.memory": "1g",
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem"
            },
        packages="org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,io.delta:delta-spark_2.12:3.2.0,org.postgresql:postgresql:42.2.20",
        dag=dag
    )

    get_data_dag >> leading_dag >> bronze_dag >> silver_dag >> gold_dag
    