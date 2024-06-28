# Ferramentas

---

## Introdução

Este documento descreve as ferramentas utilizadas no projeto, incluindo as tecnologias de banco de dados, linguagens de programação, ferramentas de orquestração de pipelines e armazenamento de objetos.

Utilizamos as seguintes ferramentas:

- **PostgreSQL** - Banco de dados relacional 
- **Python** - Linguagem de programação utilizada para criar os scripts de extração, transformação e carga de dados
- **Docker** - Containerização de aplicações
- **Apache Spark** - Processamento de dados em larga escala
- **Apache Airflow** - Orquestrador de tarefas
- **Visual Studio Code** - Editor de código
- **Astro CLI** - Ferramenta de linha de comando para gerenciamento de infraestrutura
- **Minio** - Armazenamento de objetos

## Descrição

<br>

**PostgreSQL**

O PostgreSQL é um sistema de gerenciamento de banco de dados relacional de código aberto e amplamente utilizado. Ele oferece suporte a recursos avançados de SQL e é conhecido por sua confiabilidade, escalabilidade e extensibilidade.

**Python**

Python é uma linguagem de programação de alto nível, interpretada e de propósito geral. É amplamente utilizada em ciência de dados, desenvolvimento web, automação de tarefas e muito mais. No projeto de Ecommerce, utilizamos Python para criar scripts de ETL e outras tarefas de processamento de dados.

**Docker**

Docker é uma plataforma de código aberto que facilita a criação, implantação e execução de aplicativos em contêineres. Ele permite que os desenvolvedores empacotem uma aplicação com todas as suas dependências em um contêiner, garantindo que ela funcione de forma consistente em qualquer ambiente.

**Apache Spark**

Apache Spark é um framework de processamento de dados em larga escala, conhecido por sua velocidade e facilidade de uso. Ele oferece suporte a várias linguagens de programação, incluindo Python, e é amplamente utilizado para análise de dados, machine learning e processamento de streaming.

**Apache Airflow**

Apache Airflow é uma plataforma de orquestração de pipelines de dados, que permite agendar, monitorar e executar tarefas de forma automatizada. Ele oferece suporte a fluxos de trabalho complexos e é altamente configurável, tornando-o uma escolha popular para a automação de processos de ETL e análise de dados.

**Visual Studio Code**

Visual Studio Code é um editor de código leve, poderoso e altamente personalizável, desenvolvido pela Microsoft. Ele oferece suporte a várias linguagens de programação e possui uma ampla variedade de extensões que facilitam o desenvolvimento de aplicativos e scripts.

**Astro CLI**

Astro CLI é uma ferramenta de linha de comando para gerenciamento de infraestrutura, desenvolvida pela Astronomer. Ela simplifica a implantação e o gerenciamento de pipelines de dados baseados em Apache Airflow, permitindo que os usuários criem, execute e monitorem tarefas de forma eficiente.

**Minio**

Minio é um serviço de armazenamento de objetos de código aberto, compatível com o Amazon S3. Ele oferece escalabilidade, alta disponibilidade e segurança para o armazenamento de dados não estruturados, como imagens, vídeos e arquivos de log.


## Instalação

Para instalar as ferramentas utilizadas no projeto, basta ir na raiz do projeto e executar o comando:

```bash
docker compose up 
```
