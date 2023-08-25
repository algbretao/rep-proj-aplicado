# Cria um bucket no S3.
resource "aws_s3_bucket" "datalake" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_ownership_controls" "datalake_owner" {
  bucket = aws_s3_bucket.datalake.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
  depends_on = [aws_s3_bucket.datalake]
}

resource "aws_s3_bucket_acl" "datalake_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.datalake_owner]

  bucket = aws_s3_bucket.datalake.id
  acl    = "private"
} 

# Configurações de rules do bucket criado.
resource "aws_s3_bucket_server_side_encryption_configuration" "datalake-configuration" {
  bucket = aws_s3_bucket.datalake.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
  depends_on = [aws_s3_bucket.datalake]
}

# Configura regras para bloquear o acesso anônimo ao conteúdo do bucket.
resource "aws_s3_bucket_public_access_block" "datalake_public_access_block" {
  bucket                  = aws_s3_bucket.datalake.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
  depends_on              = [aws_s3_bucket.datalake]
} 