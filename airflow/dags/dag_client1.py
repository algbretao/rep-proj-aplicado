from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.aws_glue_job import AwsGlueJobSensor
from datetime import datetime
import boto3

# Crie um cliente para o serviço AWS Glue
glue_client = boto3.client('glue', region_name='us-east-1')  # Substitua pela sua região

# Funções para execução dos Glue Jobs
def execute_glue_job_ftp_to_raw(**kwargs):
    job_name = 'glue_job_ftp_to_raw'  # Nome do Glue Job
    response = glue_client.start_job_run(JobName=job_name)
    # Captura o ID da execução do job para monitoramento

def execute_glue_job_raw_to_trusted(**kwargs):
    job_name = 'glue_job_raw_to_trusted'  # Nome do Glue Job
    response = glue_client.start_job_run(JobName=job_name)
    # Captura o ID da execução do job para monitoramento

def execute_glue_job_trusted_to_refined(**kwargs):
    job_name = 'glue_job_trusted_to_refined'  # Nome do Glue Job
    response = glue_client.start_job_run(JobName=job_name)
    # Captura o ID da execução do job para monitoramento

# Definição da DAG
dag = DAG('dag_etl_client1', schedule_interval=None, start_date=datetime(2023, 1, 1))

# Tarefas (tasks) que executam os Glue Jobs
task_ftp_to_raw = PythonOperator(
    task_id='execute_glue_job_ftp_to_raw',
    python_callable=execute_glue_job_ftp_to_raw,
    provide_context=True,
    dag=dag,
)

# task_raw_to_trusted = PythonOperator(
#     task_id='execute_glue_job_raw_to_trusted',
#     python_callable=execute_glue_job_raw_to_trusted,
#     provide_context=True,
#     dag=dag,
# )

# task_trusted_to_refined = PythonOperator(
#     task_id='execute_glue_job_trusted_to_refined',
#     python_callable=execute_glue_job_trusted_to_refined,
#     provide_context=True,
#     dag=dag,
# )

task_raw_to_trusted = AwsGlueJobSensor(
    task_id='wait_for_glue_job_raw_to_trusted',
    job_name='glue_job_raw_to_trusted',
    timeout=600,  # Tempo limite de espera
    poke_interval=60,  # Intervalo entre verificações
    aws_conn_id='aws_default',  # Conexão AWS definida no Airflow
    dag=dag,
)

task_trusted_to_refined = AwsGlueJobSensor(
    task_id='wait_for_glue_job_trusted_to_refined',
    job_name='glue_job_trusted_to_refined',
    timeout=600,  # Tempo limite de espera
    poke_interval=60,  # Intervalo entre verificações
    aws_conn_id='aws_default',  # Conexão AWS definida no Airflow
    dag=dag,
)

# # Define a ordem das tarefas na sequência
# task_ftp_to_raw >> task_raw_to_trusted >> task_trusted_to_refined

# Define a ordem das tarefas na sequência usando CrossDependency
task_ftp_to_raw.set_downstream(task_raw_to_trusted)
task_raw_to_trusted.set_downstream(task_trusted_to_refined)