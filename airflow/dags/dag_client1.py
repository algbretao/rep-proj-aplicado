from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import boto3
import time

# Crie um cliente para o serviço AWS Glue
glue_client = boto3.client('glue', region_name='us-east-1')  # Substitua pela sua região

# Função para verificar o status do Glue Job
def wait_for_job_completion(job_name, run_id):
    while True:
        response = glue_client.get_job_run(JobName=job_name, RunId=run_id)
        status = response['JobRun']['JobRunState']
        if status in ['SUCCEEDED', 'FAILED', 'STOPPED']:
            return status
        time.sleep(20)  # Aguarde 20 segundos antes de verificar novamente

# Funções para execução dos Glue Jobs atualizadas
def execute_glue_job_ftp_to_raw(**kwargs):
    job_name = 'glue_job_ftp_to_raw'
    response = glue_client.start_job_run(JobName=job_name)
    run_id = response['JobRunId']
    wait_for_job_completion(job_name, run_id)

def execute_glue_job_raw_to_trusted(**kwargs):
    job_name = 'glue_job_raw_to_trusted'
    response = glue_client.start_job_run(JobName=job_name)
    run_id = response['JobRunId']
    wait_for_job_completion(job_name, run_id)

def execute_glue_job_trusted_to_refined(**kwargs):
    job_name = 'glue_job_trusted_to_refined'
    response = glue_client.start_job_run(JobName=job_name)
    run_id = response['JobRunId']
    wait_for_job_completion(job_name, run_id)

# Definição da DAG
dag = DAG('dag_etl_client1', schedule_interval='@daily', start_date=datetime(2023, 8, 1))

# Tarefas (tasks) que executam os Glue Jobs
task_ftp_to_raw = PythonOperator(
    task_id='execute_glue_job_ftp_to_raw',
    python_callable=execute_glue_job_ftp_to_raw,
    provide_context=True,
    dag=dag,
)

task_raw_to_trusted = PythonOperator(
    task_id='execute_glue_job_raw_to_trusted',
    python_callable=execute_glue_job_raw_to_trusted,
    provide_context=True,
    dag=dag,
)

task_trusted_to_refined = PythonOperator(
    task_id='execute_glue_job_trusted_to_refined',
    python_callable=execute_glue_job_trusted_to_refined,
    provide_context=True,
    dag=dag,
)

# Define a ordem das tarefas na sequência
task_ftp_to_raw >> task_raw_to_trusted >> task_trusted_to_refined