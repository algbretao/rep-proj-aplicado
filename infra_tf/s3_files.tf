locals {
  # Cria uma lista de objetos que contêm informações sobre os jobs de glue
  glue_jobs = [for name in var.glue_job_names : {
    name     = name,                           # O nome do job atual sendo iterado
    filename = var.glue_job_file_mapping[name] # O nome do arquivo associado ao job
  }]
}

resource "aws_s3_object" "codigo_glue_job" {
  depends_on = [aws_s3_bucket.datalake]
  for_each   = { for job in local.glue_jobs : job.name => job }
  bucket     = aws_s3_bucket.datalake.id
  key        = "/scripts/${each.value.name}"                     # Diretório onde será gravado o arquivo de cada script
  source     = "../airflow/glue/${each.value.filename}"          # Arquivo com o job que vai subir no S3
  etag       = filemd5("../airflow/glue/${each.value.filename}") # Define qual é o objeto de parâmetro
} 