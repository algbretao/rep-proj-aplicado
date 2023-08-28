# from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

# # Cria uma tarefa para chamar o Glue Job chamado 'extract_data'
# extract_data_task = GlueJobOperator(
#     job_name='extract_data',
#     script_location='scripts/extract_data.py',
# )