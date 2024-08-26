from airflow.utils.dates import days_ago
from airflow.decorators import dag,task, task_group
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import RenderConfig
from include.dbt.fraud.cosmos_config import DBT_CONFIG, DBT_PROJECT_CONFIG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.models.baseoperator import chain

AIRBYTE_CONN_ID = 'bcbef634-10f5-413a-aac4-feecf4158c37'

@dag(
    start_date=days_ago(1),
    schedule='@daily',
    catchup=False,
    tags=['airbyte','dbt','elt_dreamshop_data'],
)

def ELT_dreamshop_data():
    @task_group(group_id='airbyteTaskGroup')
    def EL_proses():
        ingest_data = AirbyteTriggerSyncOperator(
            task_id='ingest_data',
            airbyte_conn_id='airbyte_conn',
            connection_id=AIRBYTE_CONN_ID,
            asynchronous=False,
            timeout=3600,
            wait_seconds=3
        )
   
        ingest_data

    @task
    def airbyte_job_done():
        return True
    
    northwind_data = DbtTaskGroup(
        group_id = "dbtTaskGroup",
        project_config = DBT_PROJECT_CONFIG,
        profile_config = DBT_CONFIG,
        render_config = RenderConfig(
            load_method = LoadMode.DBT_LS,
            select=['path:models']
        )
    )

    chain(
        EL_proses(),
        airbyte_job_done(),
        dreamshop_data
    )

ELT_northwind_data()