# Generated via https://github.com/mozilla/bigquery-etl/blob/main/bigquery_etl/query_scheduling/generate_airflow_dags.py

from airflow import DAG
from airflow.sensors.external_task import ExternalTaskMarker
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.task_group import TaskGroup
import datetime
from utils.constants import ALLOWED_STATES, FAILED_STATES
from utils.gcp import bigquery_etl_query, gke_command

docs = """
### bqetl_org_mozilla_firefox_derived

Built from bigquery-etl repo, [`dags/bqetl_org_mozilla_firefox_derived.py`](https://github.com/mozilla/bigquery-etl/blob/main/dags/bqetl_org_mozilla_firefox_derived.py)

#### Owner

frank@mozilla.com
"""


default_args = {
    "owner": "frank@mozilla.com",
    "start_date": datetime.datetime(2022, 11, 30, 0, 0),
    "end_date": None,
    "email": ["frank@mozilla.com", "telemetry-alerts@mozilla.com"],
    "depends_on_past": False,
    "retry_delay": datetime.timedelta(seconds=1800),
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 2,
}

tags = ["impact/tier_1", "repo/bigquery-etl"]

with DAG(
    "bqetl_org_mozilla_firefox_derived",
    default_args=default_args,
    schedule_interval="0 2 * * *",
    doc_md=docs,
    tags=tags,
) as dag:
    fenix_derived__attributable_clients__v1 = bigquery_etl_query(
        task_id="fenix_derived__attributable_clients__v1",
        destination_table="attributable_clients_v1",
        dataset_id="fenix_derived",
        project_id="moz-fx-data-shared-prod",
        owner="frank@mozilla.com",
        email=["frank@mozilla.com", "telemetry-alerts@mozilla.com"],
        date_partition_parameter="submission_date",
        depends_on_past=False,
    )

    with TaskGroup(
        "fenix_derived__attributable_clients__v1_external"
    ) as fenix_derived__attributable_clients__v1_external:
        ExternalTaskMarker(
            task_id="bqetl_campaign_cost_breakdowns__wait_for_fenix_derived__attributable_clients__v1",
            external_dag_id="bqetl_campaign_cost_breakdowns",
            external_task_id="wait_for_fenix_derived__attributable_clients__v1",
            execution_date="{{ (execution_date - macros.timedelta(days=-1, seconds=82800)).isoformat() }}",
        )

        fenix_derived__attributable_clients__v1_external.set_upstream(
            fenix_derived__attributable_clients__v1
        )

    fenix_derived__clients_yearly__v1 = bigquery_etl_query(
        task_id="fenix_derived__clients_yearly__v1",
        destination_table="clients_yearly_v1",
        dataset_id="fenix_derived",
        project_id="moz-fx-data-shared-prod",
        owner="frank@mozilla.com",
        email=["frank@mozilla.com", "telemetry-alerts@mozilla.com"],
        date_partition_parameter="submission_date",
        depends_on_past=True,
    )

    org_mozilla_fenix_derived__client_deduplication__v1 = bigquery_etl_query(
        task_id="org_mozilla_fenix_derived__client_deduplication__v1",
        destination_table="client_deduplication_v1",
        dataset_id="org_mozilla_fenix_derived",
        project_id="moz-fx-data-shared-prod",
        owner="frank@mozilla.com",
        email=["frank@mozilla.com", "telemetry-alerts@mozilla.com"],
        date_partition_parameter="submission_date",
        depends_on_past=False,
        arguments=["--schema_update_option=ALLOW_FIELD_ADDITION"],
    )

    org_mozilla_firefox_beta_derived__client_deduplication__v1 = bigquery_etl_query(
        task_id="org_mozilla_firefox_beta_derived__client_deduplication__v1",
        destination_table="client_deduplication_v1",
        dataset_id="org_mozilla_firefox_beta_derived",
        project_id="moz-fx-data-shared-prod",
        owner="frank@mozilla.com",
        email=["frank@mozilla.com", "telemetry-alerts@mozilla.com"],
        date_partition_parameter="submission_date",
        depends_on_past=False,
        arguments=["--schema_update_option=ALLOW_FIELD_ADDITION"],
    )

    org_mozilla_firefox_derived__client_deduplication__v1 = bigquery_etl_query(
        task_id="org_mozilla_firefox_derived__client_deduplication__v1",
        destination_table="client_deduplication_v1",
        dataset_id="org_mozilla_firefox_derived",
        project_id="moz-fx-data-shared-prod",
        owner="frank@mozilla.com",
        email=["frank@mozilla.com", "telemetry-alerts@mozilla.com"],
        date_partition_parameter="submission_date",
        depends_on_past=False,
        arguments=["--schema_update_option=ALLOW_FIELD_ADDITION"],
    )

    wait_for_baseline_clients_daily = ExternalTaskSensor(
        task_id="wait_for_baseline_clients_daily",
        external_dag_id="copy_deduplicate",
        external_task_id="baseline_clients_daily",
        execution_delta=datetime.timedelta(seconds=3600),
        check_existence=True,
        mode="reschedule",
        allowed_states=ALLOWED_STATES,
        failed_states=FAILED_STATES,
        pool="DATA_ENG_EXTERNALTASKSENSOR",
    )

    fenix_derived__attributable_clients__v1.set_upstream(
        wait_for_baseline_clients_daily
    )
    wait_for_search_derived__mobile_search_clients_daily__v1 = ExternalTaskSensor(
        task_id="wait_for_search_derived__mobile_search_clients_daily__v1",
        external_dag_id="bqetl_mobile_search",
        external_task_id="search_derived__mobile_search_clients_daily__v1",
        execution_delta=datetime.timedelta(0),
        check_existence=True,
        mode="reschedule",
        allowed_states=ALLOWED_STATES,
        failed_states=FAILED_STATES,
        pool="DATA_ENG_EXTERNALTASKSENSOR",
    )

    fenix_derived__attributable_clients__v1.set_upstream(
        wait_for_search_derived__mobile_search_clients_daily__v1
    )

    fenix_derived__clients_yearly__v1.set_upstream(wait_for_baseline_clients_daily)

    wait_for_copy_deduplicate_all = ExternalTaskSensor(
        task_id="wait_for_copy_deduplicate_all",
        external_dag_id="copy_deduplicate",
        external_task_id="copy_deduplicate_all",
        execution_delta=datetime.timedelta(seconds=3600),
        check_existence=True,
        mode="reschedule",
        allowed_states=ALLOWED_STATES,
        failed_states=FAILED_STATES,
        pool="DATA_ENG_EXTERNALTASKSENSOR",
    )

    org_mozilla_fenix_derived__client_deduplication__v1.set_upstream(
        wait_for_copy_deduplicate_all
    )

    org_mozilla_firefox_beta_derived__client_deduplication__v1.set_upstream(
        wait_for_copy_deduplicate_all
    )

    org_mozilla_firefox_derived__client_deduplication__v1.set_upstream(
        wait_for_copy_deduplicate_all
    )
