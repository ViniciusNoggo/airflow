import pandas as pd
import pendulum

from airflow.macros import ds_add
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


def extract_data(start_date: pendulum.datetime, end_date: pendulum.datetime):
    KEY = "HDK9H2FBWXDP2AN86FWLZBGFT"
    city = "Boston"
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}?key={KEY}&unitGroup=metric&include=days&contentType=csv"

    data = pd.read_csv(url)

    return data


def load_data_into_csv_file(data: pd.DataFrame, file_path: str):
    data.to_csv(path_or_buf=file_path + "dados_brutos.csv")
    data[["datetime", "tempmin", "temp", "tempmax"]].to_csv(
        path_or_buf=file_path + "temperatura.csv"
    )
    data[["datetime", "description", "icon"]].to_csv(
        path_or_buf=file_path + "condicoes.csv"
    )


def format_file_path(file_path: str, start_date: str):
    file_path = file_path.replace("\\", "")
    file_path = file_path + "/"
    return file_path


def main(start_date: str, range_date: int, file_path: str):
    end_date = ds_add(start_date, range_date)
    data = extract_data(start_date, end_date)
    file_path = format_file_path(file_path, start_date)
    load_data_into_csv_file(data, file_path)


with DAG(
    dag_id="dados_climaticos",
    start_date=pendulum.today().subtract(weeks=3),
    schedule_interval="0 0 * * 1",  # cron: minuto hora dia_do_mes mes dia_da_semana: minuto:0 hora:0
) as dag:

    FILE_PATH = "~/Área\ de\ Trabalho/airflow/pasta_criada_pelo_terceiro_dag_na_pratica_dados_climaticos/semana="

    tarefa_1 = BashOperator(
        task_id="cria_pasta",
        bash_command="mkdir -p "
        + FILE_PATH
        + '{{data_interval_end.strftime("%Y-%m-%d")}}',
    )

    tarefa_2 = PythonOperator(
        task_id="extrai_dados_API",
        python_callable=main,
        # Passar os parâmetros da função executada na task, no caso são, o Jinja template date_interval_end, o range e caminho que seram salvos os dados
        op_kwargs={
            "start_date": '{{data_interval_end.strftime("%Y-%m-%d")}}',
            "range_date": 7,
            "file_path": FILE_PATH + '{{data_interval_end.strftime("%Y-%m-%d")}}',
        },
    )

    tarefa_1 >> tarefa_2
