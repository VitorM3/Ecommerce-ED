# Padrões do projeto

---

## Documentação

Focamos em criar uma documentação concisa, utilizando os melhores padrões de escrita e organização de documentos. Para isso, utilizamos o Markdown, que é uma linguagem de marcação leve e fácil de usar, responsável tanto pelas documentações que você está lendo e as que estão disponíveis no repositório.

Os arquivos recomendados para a documentação são:

- `README.md`           - Documentação principal do projeto
- `CHANGELOG.md`        - Registro de todas as alterações feitas no projeto
- `CONTRIBUTING.md`     - Guia de contribuição para o projeto
- `CODE_OF_CONDUCT.md`  - Código de conduta para os colaboradores
- `COLABORATORS.md`     - Lista de todos os colaboradores do projeto
- `SECURITY.md`         - Informações sobre como denunciar vulnerabilidades de segurança do projeto
- `LICENSE`             - Licença do projeto

<br>

Além disso, nos atentamos em criar padrões para Issues e Pull Requests, para que a comunicação entre os colaboradores seja eficiente e clara. Os templates podem ser encontrados dentro de `.github`.


| Pull Request              | Bug Issue            | Feature Request Issue |
|---------------------------|----------------------|-----------------------|
|`PULL_REQUEST_TEMPLATE.md` | `bug-report.yml`     | `feature-request.yml` |	  

<br>

## Changelog

Tentamos criar uma pipeline (localizada em `.github/release.yml`) para automatizar a criação de releases e a atualização do `CHANGELOG.md`. A ideia é que a cada nova versão, o arquivo seja atualizado com as novas funcionalidades, correções e melhorias feitas. Porém não conseguimos criar uma release a tempo para testar o funcionamento.

<br>

## Deploy

Para o deploy do MKDocs, utilizamos o GitHub Pages. A pipeline `deploy-mkdocs.yml` dentro de `.github/workflows` é responsável por fazer o deploy automático do site a cada nova alteração feita na branch `main` e verificando somente arquivos em que há alterações que geram uma nova versão do MKDocs. A ideia é que o site seja atualizado automaticamente, sem a necessidade de intervenção humana.