-- Generated via bigquery_etl.glean_usage
CREATE OR REPLACE VIEW
  `org_mozilla_firefox.baseline_clients_daily`
AS
SELECT
  *
FROM
  `moz-fx-data-shared-prod.org_mozilla_firefox_derived.baseline_clients_daily_v1`
