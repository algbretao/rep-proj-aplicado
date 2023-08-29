# Cria o Job Glue com os parâmetros necessários, a execução do Job é manual, através do AWS Console.
resource "aws_glue_job" "glue_jobs" {
  for_each    = { for name in var.glue_job_names : name => name }
  name        = replace(each.key, "\\.py$", "") # Remover a extensão .py do nome do Job que será exibido no console.
  role_arn    = var.iam_arn                     # Está sendo selecionada a IAM role já existente, criada anteriormemte.
  max_retries = "1"                             # Máximo de tentativas de execução.
  timeout     = 2880
  command {
    # Path do bucket S3 onde está gravado o arquivo pyspark com o código do glue job a ser executado.
    script_location = "s3://${var.bucket_name}/glue/${each.value}"
    python_version  = "3"
  }
  execution_property {
    max_concurrent_runs = 1
  }
  glue_version = "3.0"
  depends_on   = [aws_s3_bucket.datalake]
}

# Cria o Crawler para indexar os dados em catálogos de dados do AWS Glue.
# Necessário dar um 'run' no Crowler através do console AWS.
resource "aws_glue_crawler" "glue_crawler_pa" {
  depends_on    = [aws_s3_bucket.datalake]
  database_name = var.database_name
  name          = var.glue_crawler_name
  role          = var.iam_arn

  s3_target {
    # Path onde o Crawler irá ler o dado já tratado no formato parquet.
    # Este path foi definido no glue job, para gravar os dados já tratados.
    path = "s3://${var.bucket_name}/refined/pa"
  }
}