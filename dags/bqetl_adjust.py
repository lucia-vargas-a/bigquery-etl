# Generated via https://github.com/mozilla/bigquery-etl/blob/main/bigquery_etl/query_scheduling/generate_airflow_dags.py

from airflow import DAG
from airflow.sensors.external_task import ExternalTaskMarker
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.task_group import TaskGroup
import datetime
from utils.constants import ALLOWED_STATES, FAILED_STATES
from utils.gcp import bigquery_etl_query, gke_command

docs = """
### bqetl_adjust

Built from bigquery-etl repo, [`dags/bqetl_adjust.py`](https://github.com/mozilla/bigquery-etl/blob/main/dags/bqetl_adjust.py)

#### Description

Derived tables built on Adjust data.
#### Owner

rbaffourawuah@mozilla.com
"""


default_args = {
    "owner": "rbaffourawuah@mozilla.com",
    "start_date": datetime.datetime(2023, 4, 25, 0, 0),
    "end_date": None,
    "email": ["telemetry-alerts@mozilla.com", "rbaffourawuah@mozilla.com"],
    "depends_on_past": False,
    "retry_delay": datetime.timedelta(seconds=1800),
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 2,
}

tags = ["impact/tier_2", "repo/bigquery-etl"]

with DAG(
    "bqetl_adjust",
    default_args=default_args,
    schedule_interval="0 4 * * *",
    doc_md=docs,
    tags=tags,
) as dag:
    adjust_derived__firefox_mobile_installs__v1 = bigquery_etl_query(
        task_id="adjust_derived__firefox_mobile_installs__v1",
        destination_table="firefox_mobile_installs_v1",
        dataset_id="adjust_derived",
        project_id="moz-fx-data-marketing-prod",
        owner="rbaffourawuah@mozilla.com",
        email=["rbaffourawuah@mozilla.com", "telemetry-alerts@mozilla.com"],
        date_partition_parameter=None,
        depends_on_past=False,
        task_concurrency=1,
    )
