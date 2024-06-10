# Pipeline de Dados

### Objetivo

O objetivo do projeto é criar uma pipeline de dados utilizando a ferramenta Airflow com o objetivo de consumir dados coletados através de webscrapping realizado no site MyAnimeList, criar procedimentos para tratamento de dados brutos e persistir os dados tratados em tabelas no bigquery com o objetivo de utilizá-las em ferramentas de visualização de dados.

### Observações

Antes de rodar o projeto será necessário criar uma contano google cloud e iniciarlizar um novo projeto no bigquery. Após isso, na área de Permissões IAM do google cloud, será necessário conceder acesso à edição e leitura aos emails associados ao projeto criado visando realizar as operações em código, logo em seguida na área **Contas e Serviços** deverá criar uma nova conta com o email vinculado ao projeto criado. Realizando esses passos será feito o download de um arquivo Json e o conteúdo do mesmo deverá ser copiado e colado no arquivo **data/bigQueryCredentials**


![image](https://github.com/Fernando-7/Pipeline_de_Dados/assets/21008992/a5f96cf9-6545-4ea0-9acf-67dd187a5f14)
