from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def cumprimentos():
    print("Boas-vindas! Primeiro script Python ativado pelo o Airflow.")


with DAG(
    dag_id="segundo_dag_python_operator",
    start_date=days_ago(1),
    schedule_interval="@daily",
) as dag:

    tarefa = PythonOperator(
        task_id="cumprimentos",
        python_callable=cumprimentos,
    )
