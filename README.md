## Construindo um ETL simples com Airflow, PostgreSQL e Docker

### Pré-requisitos:

- [VS Code](https://code.visualstudio.com/download)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [DBeaver ](https://dbeaver.io/download/)
- [Python](https://www.python.org/downloads/)


### Roteiro:

#### 1. Criando Ambiente Virtual
Dentro da pasta raiz do nosso diretorio vamos executar o seguinte comando
```bash  copy
python -m venv .venv
```

#### 2. Após isso vamos ativar nosso ambiente virtual criado com o comando acima
PowerShell 👇
```bash  copy
.venv\Scripts\Activate
```
Cmd 👇
```bash  copy
.venv\Scripts\activate.bat
```

> **Atenção:** Todo o ambiente foi configurado com o sistema operacional Windows. Em outros sistemas operacionais, os códigos podem ser diferentes.

#### 3. Navegar até a pasta onde iremos realizar as DAGs e o ETL
```bash copy
cd airflow
```

#### 4.	Configurar a Variável de Ambiente AIRFLOW_UID
Caso já tenha o arquivo .ambiente criado, editar ou excluir o mesmo
```bash  copy
$userId = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
echo "AIRFLOW_UID=$userId" > .ambiente
```

#### 5. Configurar e Iniciar o Docker Composer
```bash  copy
docker compose up airflow-init
```

#### 6. Inicializando os containers no modo desanexado
```bash copy
docker compose up -d
```

#### 7. Verificando a IU do Airflow
Agora abra seu navegador e visite https://localhost:8080/, e você deverá acessar a página de login do Airflow:
login padrão: airflow
senha padrão: airflow

#### 8. Conectando o Dbeaver!
Conforme imagem abaixo, atenção na porta que deve ser 5433:
[alt text](image.png)

##### 8.1. Em seguida, clique duas vezes no ícone SQL no canto superior esquerdo para escrever a consulta SQL, isso criará um esquema de dados no banco de dados.
```bash copy
CREATE SCHEMA data;
```

##### 9 Consultando os dados
Com a nossa estrutura pronta, agora é só finalizar as DAGs, onde vamos realizar o ETL e limpar os dados até estarem prontos para o usuário final.

> <b>Nota:</b> Referência do arquivo: https://intuitivedataguide.medium.com/building-a-simple-etl-with-airflow-postgresql-and-docker-a2b1a2b202ec. 
