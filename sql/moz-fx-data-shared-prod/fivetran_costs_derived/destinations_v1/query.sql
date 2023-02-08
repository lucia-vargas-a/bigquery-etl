SELECT
  id AS destination_id,
  name AS destination_name,
  account_id,
  created_at,
  region
FROM
  `moz-fx-data-bq-fivetran.fivetran_log.destination`
UNION ALL
SELECT
  id AS destination_id,
  name AS destination_name,
  account_id,
  created_at,
  region
FROM
  `dev-fivetran.fivetran_log.destination`
