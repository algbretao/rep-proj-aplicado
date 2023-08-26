import sys
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
import boto3
from pyspark.context import SparkContext
from pyspark.sql import functions as f

# Inicializar o contexto do Glue
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Configurações do S3
input_bucket = "datalake-pa-tf-prd"
input_prefix = "trusted/"
output_bucket = "datalake-pa-tf-prd"
output_prefix = "refined/"

try:
    # Ler o arquivo parquet da trusted
    input_path = f"s3://{input_bucket}/{input_prefix}"
    df = spark.read.parquet(input_path)

    # Fazer transformações necessárias no DataFrame
    # .....

    # Salvar o DataFrame no formato Parquet no S3, particionado por Ano_Atendimento e Mes_Atendimento
    output_path = f"s3://{output_bucket}/{output_prefix}"
    df.write.partitionBy("Ano_Atendimento", "Mes_Atendimento").parquet(output_path, mode="overwrite")
    
    # Print para indicar que o processamento foi concluído e o arquivo foi salvo
    print("Processamento concluído e arquivo salvo na pasta refined.")

except Exception as e:
    # Imprimir mensagem de erro se ocorrer uma exceção durante o processamento
    print("Ocorreu um erro durante o processamento:", str(e))

finally:
    # Finalizar o Glue Job
    job.commit()