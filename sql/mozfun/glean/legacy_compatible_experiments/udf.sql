CREATE OR REPLACE FUNCTION glean.legacy_compatible_experiments(ping_info__experiments ARRAY)
RETURNS ARRAY AS (
  ARRAY(
    SELECT
      STRUCT(x.key AS key, x.value.branch AS value)
    FROM
      UNNEST(ping_info__experiments) x
  ) AS experiments
);

                -- Tests
WITH ping_info AS (
  SELECT
    ARRAY(
      STRUCT(
        "experiment_a" AS key,
        STRUCT("control" AS branch, STRUCT("type" AS "firefox") AS extra) AS value
      ),
      STRUCT(
        "experiment_b" AS key,
        STRUCT("treatment" AS branch, STRUCT("type" AS "firefoxOS") AS extra) AS value
      ),
    ) AS experiments
),
expected AS (
  SELECT
    ARRAY(
      STRUCT("experiment_a" AS key, "control" AS value),
      STRUCT("experiment_b" AS key, "treatment" AS value),
    ) AS experiments
),
)
SELECT
  assert.equals(expected, glean.legacy_compatible_experiments(ping_info.experiments))
