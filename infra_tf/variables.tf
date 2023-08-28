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

variable "glue_job_names" {
  type = list(string)
  default = [
    "glue_job_ftp_to_raw.py",
    "glue_job_raw_to_trusted.py",
    "glue_job_trusted_to_refined.py",
  ]
}

variable "glue_job_file_mapping" {
  type = map(string)
  default = {
    "glue_job_ftp_to_raw.py"         = "ftp_to_raw_s3.py",
    "glue_job_raw_to_trusted.py"     = "raw_to_trusted_s3.py",
    "glue_job_trusted_to_refined.py" = "trusted_to_refined_s3.py",
  }
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
  default = "small"
}

variable "executor_type_mwaa" {
  default = "local"
}

variable "dag_s3_path_mwaa" {
  default = "dags"
}

variable "vpc_mwaa" {
  default = "vpc-01362a5a046cb99c8"  
}

variable "subnets_mwaa" {
  type = list(string)
  default = ["subnet-0101f7386c75f0e7d", "subnet-0dac3d0bdda62b4c9"]
}

variable "kms_key_id_mwaa" {
  default = "arn:aws:kms:us-east-1:451237051222:key/daf6c528-3766-4b5b-a3ba-b6ece535dfc6"
}