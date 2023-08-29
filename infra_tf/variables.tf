variable "regiao" {
  default = "us-east-1"
}

variable "bucket_name" {
  default = "datalake-pa-tf-prd"
}

# URI da IAM Role criada no AWS.
variable "iam_arn" {
  default = "arn:aws:iam::451237051222:role/AWSGlueServiceRole-admin"
}

variable "dag_file_names" {
  type = list(string)
  default = [
    "dag_ftp_to_raw.py",
    "dag_raw_to_trusted.py",
    "dag_trusted_to_refined.py",
  ]
}


variable "glue_job_names" {
  type = list(string)
  default = [
    "glue_job_ftp_to_raw.py",
    "glue_job_raw_to_trusted.py",
    "glue_job_trusted_to_refined.py",
  ]
}

variable "glue_key_path" {
  default = "glue-code/pyspark/"
}

variable "database_name" {
  default = "database-proj-apl"
}

variable "glue_crawler_name" {
  default = "glue_crawler_proj_apl"
}

variable "cluster_name_mwaa" {
  default = "mwaa-cluster-airflow"
}

variable "cluster_size_mwaa" {
  default = "mw1.small"
}

variable "dag_s3_path_mwaa" {
  default = "dags"
}

variable "security_group_mwaa" {
  type    = list(string)
  default = ["sg-0785f73b47ebfed05"]
}

variable "log_level_mwaa" {
  default = "INFO"
}

variable "subnets_mwaa" {
  type    = list(string)
  default = ["subnet-0101f7386c75f0e7d", "subnet-0dac3d0bdda62b4c9"]
}

variable "source_bucket_arn" {
  default = "arn:aws:s3:::datalake-pa-tf-prd"
}

variable "webserver_access_mode" {
  default = "PUBLIC_ONLY"
}