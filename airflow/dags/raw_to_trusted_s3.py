import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
import boto3
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions

## @params: [JOB_NAME] 
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()

# Inicializar o contexto do Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Obter opções resolvidas
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Configurações do AWS S3
aws_access_key = "AKIAWSD6S7NLBI4OU3X2"
aws_secret_key = "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"
aws_region = "us-east-1"

# Configurações do S3
input_bucket = "datalake-pa-tf-prd"
input_prefix = "raw/"
output_bucket = "datalake-pa-tf-prd"
output_prefix = "trusted/"

# Configurar as credenciais da AWS
spark.conf.set("spark.hadoop.fs.s3a.access.key", aws_access_key)
spark.conf.set("spark.hadoop.fs.s3a.secret.key", aws_secret_key)
spark.conf.set("spark.hadoop.fs.s3a.endpoint", f"s3a://{aws_region}")

# Ler o arquivo CSV do S3
input_path = f"s3a://{input_bucket}/{input_prefix}"
df = spark.read.option("header", "true").csv(input_path)

# Fazer transformações ou processamentos no DataFrame, se necessário

# Salvar o DataFrame no formato Parquet no S3
output_path = f"s3a://{output_bucket}/{output_prefix}"
df.write.parquet(output_path, mode="overwrite")

job.commit() # Apagar se der erro