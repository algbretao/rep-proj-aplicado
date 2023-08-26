import sys
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
import boto3
from pyspark.context import SparkContext
from pyspark.sql import functions as f
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import hashlib
import random

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

# Hashing para documentos
def hash_document(number):
    hash_algorithm = hashlib.sha256()
    number_bytes = str(number).encode('utf-8')
    hash_algorithm.update(number_bytes)
    hashed_value = hash_algorithm.hexdigest()
    return hashed_value

# Função para anonimizar nomes
def mask_name(razao_social):
    words = razao_social.split(" ")
    for i in range(len(words)):
        words[i] = "*" * random.randint(1, len(words[i])) + words[i][random.randint(2, len(words[i]) - 2)] + "*" * random.randint(1, len(words[i]))
    return " ".join(words)

try:
    # Ler o arquivo parquet da trusted
    input_path = f"s3://{input_bucket}/{input_prefix}"
    df = spark.read.parquet(input_path)

    df.show(5)

    # Aplicar a UDF aos campos de documentos
    hash_udf = udf(hash_document, StringType())
    df_with_hashed_fields = df.withColumn("Registro_ANS_Hashed", hash_udf(df["Registro_ANS"])) \
                              .withColumn("Numero_Demanda_Hashed", hash_udf(df["Numero_Demanda"]))

    # Drop dos campos originais de documentos no DataFrame
    df_with_hashed_fields = df_with_hashed_fields.drop("Registro_ANS", "Numero_Demanda")

    df_with_hashed_fields.show(5)

    # Aplicar UDF ao campo de razão social
    mask_names_udf = udf(mask_name, StringType())
    df_anonymized = df_with_hashed_fields.withColumn("Razao_Social_Anonymized", mask_names_udf(df_with_hashed_fields["Razao_Social"]))

    # Drop do campo original de razão social no DataFrame
    df_anonymized = df_anonymized.drop("Razao_Social")

    # Salvar o DataFrame no formato Parquet no S3, particionado por Ano_Atendimento e Mes_Atendimento
    output_path = f"s3://{output_bucket}/{output_prefix}"
    df_anonymized.write.partitionBy("Ano_Atendimento", "Mes_Atendimento").parquet(output_path, mode="overwrite")

    df_anonymized.show(5)
    
    # Print para indicar que o processamento foi concluído e o arquivo foi salvo
    print("Processamento concluído e arquivo salvo na pasta refined.")

except Exception as e:
    # Imprimir mensagem de erro se ocorrer uma exceção durante o processamento
    print("Ocorreu um erro durante o processamento:", str(e))

finally:
    # Finalizar o Glue Job
    job.commit()