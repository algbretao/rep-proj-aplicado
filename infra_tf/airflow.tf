resource "mwaa_cluster" "mwaa_cluster_airflow" {
  name = var.cluster_name_mwaa
  size = var.cluster_size_mwaa
  executor_type = var.executor_type_mwaa

  encryption_configuration {
    kms_key_id = var.kms_key_id_mwaa
  }

  mwaa_dags_s3_bucket {
    bucket_name = var.bucket_name
    dag_s3_path = var.dag_s3_path_mwaa
  }

  vpc_id = var.vpc_mwaa
  subnets = var.subnets_mwaa

  airflow_min_workers = 1
  airflow_max_workers = 4
  airflow_scheduler_count = 1
  airflow_logs_bucket = var.bucket_name
  airflow_execution_role_arn = var.iam_arn
}