# Projeto Aplicado - mba Engenharia de Dados

## Infraestrutura na AWS, criada automaticamente via Terraform

### IaC com esteiras de Deploy, utilizando o Github 

1. Criação de um bucket no S3 da AWS, com criptografia "AES256" e não público. <br>

2. Criação de Glue Job na AWS para extrair dados de um servidor FTP e carregar na raw do Bucket S3.  <br>

3. Criação de Glue Job na AWS para processar os dados na raw e salvar na trusted do Bucket S3.  <br>

4. Criação de Glue Job na AWS para processar os dados na trusted e salvar na refined do Bucket S3.  <br>

5. Criação de um Glue Crawler para indexar os dados na refined em catálogos de dados do AWS Glue.


### Após execução da IaC

1. Dar um "Run" no Crawler criado na AWS via terraform.

1. Executar a DAG do Airflow para iniciar o processo automático de ingestão de dados. <br>

3. Fazer integração com o AWS Athena (engine de Data Lake) para analisar os dados da refined com comandos SQL.


### Desenho da Arquitetura

![AWS Iac Terraform](/img/dgm_arquitetura.png)‣敲⵰慰 