resource "aws_mwaa_environment" "mwaa_cluster_airflow" {
  name               = var.cluster_name_mwaa
  dag_s3_path        = var.dag_s3_path_mwaa
  execution_role_arn = var.iam_arn
  source_bucket_arn  = var.source_bucket_arn
  environment_class  = var.cluster_size_mwaa

  network_configuration {
    security_group_ids = var.security_group_mwaa
    subnet_ids         = var.subnets_mwaa
  }

  logging_configuration {
    dag_processing_logs {
      enabled = true # Habilitar a coleta de logs para processamento de DAGs
    }
    scheduler_logs {
      enabled = true # Habilitar a coleta de logs para os agendadores
    }
    task_logs {
      enabled = true # Habilitar a coleta de logs para tarefas DAG
    }
    webserver_logs {
      enabled = true # Habilitar a coleta de logs para os servidores web
    }
    worker_logs {
      enabled = true # Habilitar a coleta de logs para os trabalhadores
    }
  }
}