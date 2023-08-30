import sys
import ftplib
import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import zipfile
import tempfile
import datetime
from pyspark.context import SparkContext
from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()

# Função para obter segredos do AWS Secrets Manager
def get_secret(secret_name, region_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return json.loads(get_secret_value_response['SecretString'])
    except ClientError as e:
        raise e  # Pode-se também adicionar logging ou outras ações aqui

# Recuperar segredos do AWS Secrets Manager
try:
    secrets = get_secret('secret-client1', 'us-east-1')
    ftp_server = secrets['FTP_SERVER']
    ftp_path = secrets['FTP_PATH']
    ftp_username = secrets['FTP_USERNAME']
    ftp_password = secrets['FTP_PASSWORD']
except ClientError as e:
    print(f"Erro ao recuperar segredo: {e}")
    sys.exit(1)

# Nome do cliente
ftp_client_name = 'client1'

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()

# Configurações do S3
s3_bucket_name = 'datalake-pa-tf-prd'
s3_folder_path = 'raw/'

# Conexão com o FTP
ftp = ftplib.FTP(ftp_server)
ftp.login(ftp_username, ftp_password)
ftp.cwd(ftp_path)
files = ftp.nlst()

# Configurações do S3 
s3 = boto3.client('s3')

# Diretório temporário
temp_dir = tempfile.mkdtemp()

# Loop para baixar e enviar os arquivos do FTP para o S3 
for file in files:
    file_path = os.path.join(ftp_path, file)  # Caminho completo no FTP
    local_file_path = os.path.join(temp_dir, file)  # Caminho local temporário

    with open(local_file_path, 'wb') as local_file:
        ftp.retrbinary('RETR ' + file_path, local_file.write)

    # Verificar se o arquivo está compactado e descompactar
    if file.lower().endswith('.zip'):
        with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

    # Enviar os arquivos para o S3
    extracted_files = [f for f in os.listdir(temp_dir) if not f.lower().endswith('.zip')]
    for extracted_file in extracted_files:
        extracted_file_path = os.path.join(temp_dir, extracted_file)
        # Renomear o arquivo com o valor de ftp_client_name
        new_extracted_file_path = os.path.join(temp_dir, ftp_client_name)
        os.rename(extracted_file_path, new_extracted_file_path)
        # Obter a extensão do arquivo original
        original_extension = os.path.splitext(extracted_file)[1]
        # Criar um novo nome de arquivo baseado na data/hora, ftp_client_name e extensão
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        new_s3_file_name = f"{timestamp}_{ftp_client_name}{original_extension}"
        s3_file_path = os.path.join(s3_folder_path, new_s3_file_name)
        try:
            s3.upload_file(new_extracted_file_path, s3_bucket_name, s3_file_path)
            print(f'Arquivo {new_s3_file_name} enviado para o S3 com sucesso.')
        except NoCredentialsError:
            print('Credenciais do S3 não configuradas corretamente.')

    os.remove(local_file_path) # Remover o arquivo local temporário

# Remover o diretório temporário e fechar a conexão FTP
for root, dirs, files in os.walk(temp_dir, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir(temp_dir)
ftp.quit()

job.commit() # Apagar se der erro