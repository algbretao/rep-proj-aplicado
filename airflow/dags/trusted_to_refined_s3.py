import sys
import os
import boto3
from botocore.exceptions import NoCredentialsError
import tempfile
import datetime
from pyspark.context import SparkContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as f
from pyspark.sql import SparkSession

## @params: [JOB_NAME] 
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()

# rais = (spark.read
# .format("csv")
# .option("header", "true")
# .option("sep", ";")
# .option("encoding","latin1")
# .option("inferSchema", "true")
# .load("s3://datalake-desafio-algbretao-tf-prd/RAIS-2020/raw/"))

# rais = (
# rais
# .withColumnRenamed('Bairros SP', 'bairros_sp')
# .withColumnRenamed('Bairros Fortaleza', 'bairros_fortaleza')
# .withColumnRenamed('Bairros RJ', 'bairros_rj')
# .withColumnRenamed('Causa Afastamento 1', 'causa_afastamento_1')
# .withColumnRenamed('Causa Afastamento 2', 'causa_afastamento_2')
# .withColumnRenamed('Causa Afastamento 3', 'causa_afastamento_3')
# .withColumnRenamed('Motivo Desligamento', 'motivo_desligamento')
# .withColumnRenamed(rais.columns[7], 'cbo_ocupacao_2002')
# .withColumnRenamed('CNAE 2.0 Classe', 'cnae_2_0_classe')
# .withColumnRenamed('CNAE 95 Classe', 'cnae_95_classe')
# .withColumnRenamed('Distritos SP', 'distritos_sp')
# .withColumnRenamed(rais.columns[11], 'vinculo_ativo_31_12')
# .withColumnRenamed(rais.columns[12], 'faixa_etaria')
# .withColumnRenamed('Faixa Hora Contrat', 'faixa_hora_contrat')
# .withColumnRenamed('Faixa Remun Dezem (SM)', 'faixa_remun_dezem_sm')
# .withColumnRenamed(rais.columns[15], 'faixa_remun_media_sm')
# .withColumnRenamed('Faixa Tempo Emprego', 'faixa_tempo_emprego')
# .withColumnRenamed(rais.columns[17], 'escolaridade_apos_2005')
# .withColumnRenamed('Qtd Hora Contr', 'qtd_hora_contr')
# .withColumnRenamed('Idade', 'idade')
# .withColumnRenamed('Ind CEI Vinculado', 'ind_cei_vinculado')
# .withColumnRenamed('Ind Simples', 'ind_simples')
# .withColumnRenamed(rais.columns[22], 'mes_admissao')
# .withColumnRenamed(rais.columns[23], 'mes_desligamento')
# .withColumnRenamed('Mun Trab', 'mun_trab')
# .withColumnRenamed(rais.columns[25], 'municipio')
# .withColumnRenamed('Nacionalidade', 'nacionalidade')
# .withColumnRenamed(rais.columns[27], 'natureza_juridica')
# .withColumnRenamed('Ind Portador Defic', 'ind_portador_defic')
# .withColumnRenamed('Qtd Dias Afastamento', 'qtd_dias_afastamento')
# .withColumnRenamed(rais.columns[30], 'raca_cor')
# .withColumnRenamed(rais.columns[31], 'regioes_adm_df')
# .withColumnRenamed('Vl Remun Dezembro Nom', 'vl_remun_dezembro_nom')
# .withColumnRenamed('Vl Remun Dezembro (SM)', 'vl_remun_dezembro_sm')
# .withColumnRenamed(rais.columns[34], 'vl_remun_media_nom')
# .withColumnRenamed(rais.columns[35], 'vl_remun_media_sm')
# .withColumnRenamed('CNAE 2.0 Subclasse', 'cnae_2_0_subclasse')
# .withColumnRenamed('Sexo Trabalhador', 'sexo_trabalhador')
# .withColumnRenamed('Tamanho Estabelecimento', 'tamanho_estabelecimento')
# .withColumnRenamed('Tempo Emprego', 'tempo_emprego')
# .withColumnRenamed(rais.columns[40], 'tipo_admissao')
# .withColumnRenamed('Tipo Estab41', 'tipo_estab41')
# .withColumnRenamed('Tipo Estab42', 'tipo_estab42')
# .withColumnRenamed('Tipo Defic', 'tipo_defic')
# .withColumnRenamed(rais.columns[44], 'tipo_vinculo')
# .withColumnRenamed('IBGE Subsetor', 'ibge_subsetor')
# .withColumnRenamed('Vl Rem Janeiro SC', 'vl_rem_janeiro_sc')
# .withColumnRenamed('Vl Rem Fevereiro SC', 'vl_rem_fevereiro_sc')
# .withColumnRenamed(rais.columns[48], 'vl_rem_marco_sc')
# .withColumnRenamed('Vl Rem Abril SC', 'vl_rem_abril_sc')
# .withColumnRenamed('Vl Rem Maio SC', 'vl_rem_maio_sc')
# .withColumnRenamed('Vl Rem Junho SC', 'vl_rem_junho_sc')
# .withColumnRenamed('Vl Rem Julho SC', 'vl_rem_julho_sc')
# .withColumnRenamed('Vl Rem Agosto SC', 'vl_rem_agosto_sc')
# .withColumnRenamed('Vl Rem Setembro SC', 'vl_rem_setembro_sc')
# .withColumnRenamed('Vl Rem Outubro SC', 'vl_rem_outubro_sc')
# .withColumnRenamed('Vl Rem Novembro SC', 'vl_rem_novembro_sc')
# .withColumnRenamed('Ano Chegada Brasil', 'ano_chegada_brasil')
# .withColumnRenamed('Ind Trab Intermitente', 'ind_trab_intermitente')
# .withColumnRenamed('Ind Trab Parcial', 'ind_trab_parcial')
# .withColumn("ano", f.lit("2020").cast('int'))
# )
# from py4j.java_gateway import java_import
# java_import(spark._sc._jvm, "org.apache.spark.sql.api.python.*")

# rais = rais.withColumn("uf", f.col("municipio").cast('string').substr(1,2).cast('int'))

# rais = (
# rais
# .withColumn("mes_desligamento", f.col('mes_desligamento').cast('int'))
# .withColumn("vl_remun_dezembro_nom", f.regexp_replace("vl_remun_dezembro_nom", ',', '.').cast('double'))
# .withColumn("vl_remun_dezembro_sm", f.regexp_replace("vl_remun_dezembro_sm", ',', '.').cast('double'))
# .withColumn("vl_remun_media_nom", f.regexp_replace("vl_remun_media_nom", ',', '.').cast('double'))
# .withColumn("vl_remun_media_sm", f.regexp_replace("vl_remun_media_sm", ',', '.').cast('double'))
# .withColumn("vl_rem_janeiro_sc", f.regexp_replace("vl_rem_janeiro_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_fevereiro_sc", f.regexp_replace("vl_rem_fevereiro_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_marco_sc", f.regexp_replace("vl_rem_marco_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_abril_sc", f.regexp_replace("vl_rem_abril_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_maio_sc", f.regexp_replace("vl_rem_maio_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_junho_sc", f.regexp_replace("vl_rem_junho_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_julho_sc", f.regexp_replace("vl_rem_julho_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_agosto_sc", f.regexp_replace("vl_rem_agosto_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_setembro_sc", f.regexp_replace("vl_rem_setembro_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_outubro_sc", f.regexp_replace("vl_rem_outubro_sc", ',', '.').cast('double'))
# .withColumn("vl_rem_novembro_sc", f.regexp_replace("vl_rem_novembro_sc", ',', '.').cast('double'))
# )

# (
# rais
# .coalesce(50)
# .write.mode('overwrite')
# .partitionBy('ano', 'uf')
# .format('parquet')
# .save('s3://datalake-pa-tf-prd/refined/pa')
# )

# job.commit()