# ETL

## Introdução
O Processo de ETL consiste em enviar dados de uma base para outra (ou para um data lake) da forma mais otimizada possível e realizando as devidas formatações e transformações.

## Ferramentas

- Apache Airflow   - Ferramenta de orquestração de pipelines
- Apache Spark     - Ferramenta de processamento de dados
- PySpark          - Biblioteca Python para processamento de dados
- MiniO            - Object Storage
- PostgreSql       - Banco de dados relacional

## Passos Executados

1. Através do Apache Airflow nós realizamos a chamada de uma Dag (processo de pipeline que neste caso será utilizado para realizar o envio de dados de uma base de dados de Ecommerce para uma base de dados dimensional), possibilitando assim, melhor análise dos dados. A Dag ETL (Dag configurada no Airflow para realizar esta operação) realizará a chamada do processo **etl_get_data** que tem como objetivo buscar os dados do banco PostgreSql e criar arquivos `.csv` contendo 1000 dados cada, facilitando assim a leitura destes.

2. Após o processo **etl_get_data** ser concluido, realizamos a chamada do processo **etl_leading**, que tem como objetivo ler os arquivos `.csv` contendo os dados do banco e enviar eles para o **MiniO** que neste contexto servirá como Object Storage. Estes arquivos são salvos no MiniO no formato `parquet`.

3. Sendo concluido o processo da camada leading, o Airflow realiza a chamada do processo **etl_bronze** que tem como objetivo ler os arquivos `parquet` e criar uma **Delta Table** destes, otimizando assim as consultas subsequentes.

4. Posteriormente, será chamado o processo **etl_silver** que será responsável pela transformação dos dados nos padrões necessários

5. Último processo dentro da arquitetura medalhão, o **etl_gold**, que enviará os dados que estão nas tabelas delta para o banco dimensional **PostgreSql**.