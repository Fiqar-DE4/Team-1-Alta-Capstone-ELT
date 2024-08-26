from datetime import datetime
from airflow.decorators import dag
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator

@dag(
    start_date=datetime(2024, 5, 14),
    schedule='@daily',
    catchup=False,
    tags=['airbyte', 'airflow'],
)
def dataIngestion():
    # Tugas untuk memindahkan data dari PostgreSQL ke BigQuery
    postgres_to_bigquery = AirbyteTriggerSyncOperator(
        task_id='ingest_postgres_to_bigquery',
        airbyte_conn_id='airbyte_conn',
        connection_id='bcbef634-10f5-413a-aac4-feecf4158c37',  # Disesuaikan dengan ID koneksi yang benar
        asynchronous=False,
        timeout=3600,
        wait_seconds=3,
    )

    postgres_to_bigquery

dataIngestion()
