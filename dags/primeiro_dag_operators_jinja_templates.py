from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

# Uma das formas de criar um DAG: context manager
with DAG(
    dag_id="primeiro_dag_operators_jinja_templates",  # Nome do DAG na interface do Airflow
    start_date=days_ago(
        2
    ),  # A partir de qualquer data será iníciado, exemplo, se quer que rode no dia atual, deve ser configurado para o dia anterior
    schedule_interval="@daily",  # Intervalo que deve ser rodado, exemplo, diariamente a meia noite: @daily
) as dag:

    # Operadores: são classes em Python com códigos encapsulados que servem para realizar tarefas. Cada instância é uma Task.

    # EmptyOperator(): utilizado apenas para utilizar o fluxo de tarefas no DAG, ou seja, é utilizado no Scheduler, para definir fluxos, mas não chegas a ser executado pelo o Executer.
    # BashOperator(): É um operador que permite executar um Script ou comando Bash.
    # PythonOperator(): executa uma função Python;
    # KubernetesPodOperator(): executa uma imagem definida como imagem do Docker em um pod do Kubernetes;
    # SnowflakeOperator(): executa uma consulta em um banco de dados Snowflake;
    # EmailOperator(): envia um e-mail.

    # Características:
    # 1) Idempotência: independentemente de quantas vezes uma tarefa for executada com os mesmos parâmetros, o resultado final deve ser sempre o mesmo;

    # 2) Isolamento: a tarefa não compartilha recursos com outras tarefas de qualquer outro operador;

    # 3) Atomicidade: a tarefa é um processo indivisível e bem determinado.

    tarefa_1 = EmptyOperator(
        task_id="tarefa_1",  # Nome da tarefa na interface do Airflow
    )

    tarefa_2 = EmptyOperator(
        task_id="tarefa_2",  # Nome da tarefa na interface do Airflow
    )

    tarefa_3 = EmptyOperator(
        task_id="tarefa_3",  # Nome da tarefa na interface do Airflow
    )

    tarefa_4 = BashOperator(
        task_id="cria_pasta",  # Nome da tarefa na interface do Airflow
        bash_command="mkdir -p ~/Área\ de\ Trabalho/airflow/pasta_criada_pelo_primeiro_dag_operators_jinja_templates/data={{data_interval_end}}",  # Comando bash que será realizado + Jinja Template, que são os metadados dos DAGs, nesse caso o metadado é o horário de execução do DAG: data_interval_end. Há outras variáveis que podem ser buscadas pelo Jinja Template do Airflow: https://airflow.apache.org/docs/apache-airflow/2.3.2/templates-ref.html
    )

    tarefa_1 >> [tarefa_2, tarefa_3]
    tarefa_3 >> tarefa_4


# DAG (Directed Acyclic Graph): fluxo de trabalho definido em Python.
# Task: unidade mais básica de um DAG. (função)
# Operator: encapsula a lógica para fazer uma unidade de trabalho (task). (função main)

# Componentes do Airflow: precisam estar em execução para que funcione corretamente
# Webserver: apresenta uma interface de usuário que nos permite inspecionar, acionar e acompanhar o comportamento dos DAGs e suas tarefas;
# Pasta de arquivos DAG: armazena os arquivos DAGs criados. Ela é lida pelo agendador e executor;
# Scheduler (agendador): lida com o acionamento dos fluxos de trabalho (DAGs) agendados e o envio de tarefas para o executor;
# Banco de dados: usado pelo agendador, executor e webserver para armazenar os metadados e status do DAG e suas tarefas;
# Executor: lida com as tarefas em execução. O Airflow possui vários executores, mas apenas um é utilizado por vez.
# Worker: processo que executa as tarefas conforme definido pelo executor. Dependendo do executor escolhido, você pode ou não ter workers (trabalhadores) como parte da infraestrutura do Airflow.
# Como se interligam? https://cursos.alura.com.br/course/apache-airflow-primeiro-pipeline-dados/task/115408 Minuto: 1:40
