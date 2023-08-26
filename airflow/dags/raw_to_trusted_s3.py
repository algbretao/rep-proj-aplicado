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
input_prefix = "raw/"
output_bucket = "datalake-pa-tf-prd"
output_prefix = "trusted/"

try:
    # Ler o arquivo CSV do S3 com encoding ISO-8859-1
    input_path = f"s3://{input_bucket}/{input_prefix}"
    df = spark.read.option("header", "true").option("delimiter", ";").option("encoding", "ISO-8859-1").csv(input_path)

    # Transformações necessárias no DataFrame

    # Renomear as colunas para nomes válidos
    new_column_names = [
        "Registro_ANS", "Razao_Social", "Beneficiarios", "Numero_Demanda",
        "Data_Atendimento", "Classificacao", "Natureza_Demanda",
        "Subtema_Demanda", "Competencia", "Data_Atualizacao"
    ]
    df = df.toDF(*new_column_names)

    # Criar a coluna Ano_Atendimento utilizando a posição 7 a 10 do campo Data_Atendimento
    df = df.withColumn("Ano_Atendimento", f.substring("Data_Atendimento", 7, 4))

    # Criar a coluna Mes_Atendimento utilizando a posição 4 a 5 do campo Data_Atendimento
    df = df.withColumn("Mes_Atendimento", f.substring("Data_Atendimento", 4, 2))

    # Salvar o DataFrame no formato Parquet no S3, particionado por Ano_Atendimento e Mes_Atendimento
    output_path = f"s3://{output_bucket}/{output_prefix}"
    df.write.partitionBy("Ano_Atendimento", "Mes_Atendimento").parquet(output_path, mode="overwrite")
    
    # Print para indicar que o processamento foi concluído e o arquivo foi salvo
    print("Processamento concluído e arquivo salvo na pasta trusted.")

except Exception as e:
    # Imprimir mensagem de erro se ocorrer uma exceção durante o processamento
    print("Ocorreu um erro durante o processamento:", str(e))

finally:
    # Finalizar o Glue Job
    job.commit()