resource "aws_s3_object" "codigo_glue_job" {
  depends_on = [aws_s3_bucket.datalake]
  for_each   = { for name in var.glue_job_names : name => name }
  bucket     = aws_s3_bucket.datalake.id
  key        = "/glue/${each.value}"                    # Diretório onde será gravado o arquivo de cada script
  source     = "../airflow/glue/${each.value}"          # Arquivo com o job que vai subir no S3
  etag       = filemd5("../airflow/glue/${each.value}") # Define qual é o objeto de parâmetro
}

resource "aws_s3_object" "dag_files" {
  depends_on = [aws_s3_bucket.datalake]
  for_each   = { for name in var.dag_file_names : name => name }
  bucket     = aws_s3_bucket.datalake.id
  key        = "/dags/${each.value}"                    # Diretório onde será gravado o arquivo de cada script
  source     = "../airflow/dags/${each.value}"          # Arquivo com o job que vai subir no S3
  etag       = filemd5("../airflow/dags/${each.value}") # Define qual é o objeto de parâmetro
}