## importar módulos
import pandas as pd
from airflow import DAG
import airflow
from airflow.operators.python import PythonOperator
import json
import requests
from datetime import datetime
import psycopg2
from sqlalchemy import create_engine

# definir credenciais do banco de dados para conexão
HOST_NAME = 'recalls_db'
DATABASE = 'recalls_db'
USER_NAME = 'admin'
PASSWORD = 'admin'
PORT_ID = 5432

# definir URL para chamada de dados do site de dados do governo
raw_url = 'https://recalls-rappels.canada.ca/sites/default/files/opendata-donneesouvertes/HCRSAMOpenData.json'

# caminho dos dados para salvar dados brutos e dados limpos
raw_data_path = '..\..\data\raw\recalls_raw.csv'
cleaned_data_path = '..\..\data\cleaned\recalls_cleaned.csv'

# definir uma variável de DAG com base no objeto Airflow DAG
dag = DAG(
    dag_id='recalls_etl_v1',
    start_date=airflow.utils.dates.days_ago(0),
    schedule_interval=None
)

# definir a função de extração que recebe a URL da API
# e salva os dados brutos como um arquivo CSV
def get_recall_data(url, raw_output_path):
    response = requests.get(url)
    response_data = response.json()
    print(response)

    recall_list = []

    for r in response_data:
        recall = {
            'recall_id': r['NID'],
            # 'title': r['Title'],
            'organization': r['Organization'],
            'product_name': r['Product'],
            'issue': r['Issue'],
            'category': r['Category'],
            'updated_at': r['Last updated']
        }
        recall_list.append(recall)

    print(f"Adicionados {len(recall_list)} registros de recalls.")

    recall_df = pd.DataFrame(recall_list)

    current_timestamp = datetime.now()

    recall_df['data_recebida_em'] = current_timestamp

    recall_df.to_csv(raw_output_path, index=False)

# definir uma função de transformação e salvar os dados limpos em outro CSV
def clean_recall_data(raw_input_path, cleaned_output_path):
    df = pd.read_csv(raw_input_path)

    df[['issue_category', 'category']] = df['category'].str.split(' - ', n=1, expand=True)
    df['updated_at'] = pd.to_datetime(df['updated_at'], format='%Y-%m-%d')

    df = df.sort_values(by=['updated_at'], ascending=False)
    df.to_csv(cleaned_output_path, index=False)

    print(f"Sucesso: dados de {len(df)} registros de recall limpos.")

# definir uma função para carregar os dados no banco de dados PostgreSQL
# e usar pd.sql() para carregar os dados transformados diretamente no banco de dados
def load_to_db(db_host, db_name, db_user, db_pswd, db_port, data_path):
    df = pd.read_csv(data_path)
    current_timestamp = datetime.now()
    df['data_ingestada_em'] = current_timestamp

    # carregar dados CSV para o banco de dados
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pswd}@{db_host}/{db_name}")
    df.to_sql('recalls', con=engine, schema='data', if_exists='replace', index=False)

    print(f"Sucesso: carregados {len(df)} registros de recall para {db_name}.")

# definir tarefa usando PythonOperator do Airflow para extração de dados brutos
get_raw_data = PythonOperator(
    task_id='get_raw_data',
    python_callable=get_recall_data,
    op_kwargs={
        'url': raw_url,
        'raw_output_path': raw_data_path
    },
    dag=dag,
)

# definir tarefas para transformar dados brutos
clean_raw_data = PythonOperator(
    task_id='clean_raw_data',
    python_callable=clean_recall_data,
    op_kwargs={
        'raw_input_path': raw_data_path,
        'cleaned_output_path': cleaned_data_path
    },
    dag=dag,
)

# definir tarefa usando PythonOperator do Airflow para carregar dados limpos no banco de dados PostgreSQL
load_data_to_db = PythonOperator(
    task_id='load_data_to_db',
    python_callable=load_to_db,
    op_kwargs={
        'db_host': HOST_NAME,
        'db_name': DATABASE,
        'db_user': USER_NAME,
        'db_pswd': PASSWORD,
        'db_port': PORT_ID,
        'data_path': cleaned_data_path
    },
    dag=dag,
)

# definir a ordem para executar cada uma das tarefas no DAG
get_raw_data >> clean_raw_data >> load_data_to_db
