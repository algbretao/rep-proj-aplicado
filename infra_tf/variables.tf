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
  default = "database-pa"
}

variable "glue_crawler_name" {
  default = "glue_crawler_pa"
}