provider "aws" {
  region = var.regiao
}

provider "mwaa" {
  region = "us-east-1"
}

# Centralizar o arquivo de controle de estado do terraform
terraform {
  backend "s3" {
    bucket = "terraform-state-pa"
    key    = "state/pa/terraform.tfstate"
    region = "us-east-1"
  }
} 

terraform {
  required_providers {
    aws = "~> 3.77.0"
    mwaa = "~> 3.0.0"
  }
}