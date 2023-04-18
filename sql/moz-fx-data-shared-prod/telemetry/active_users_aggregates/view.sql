CREATE OR REPLACE VIEW
  `moz-fx-data-shared-prod.telemetry.active_users_aggregates`
AS
SELECT
  segment,
  attribution_medium,
  attribution_source,
  attributed,
  city,
  country,
  distribution_id,
  first_seen_year,
  is_default_browser,
  channel,
  os,
  os_version,
  os_version_major,
  os_version_minor,
  submission_date,
  language_name,
  dau,
  wau,
  mau,
  new_profiles,
  ad_clicks,
  organic_search_count,
  search_count,
  search_with_ads,
  uri_count,
  active_hours,
  app_name,
  app_version,
  app_version_major,
  app_version_minor,
  app_version_patch_revision,
  app_version_is_major_release
FROM
  `moz-fx-data-shared-prod.telemetry.active_users_aggregates_mobile`
UNION ALL
SELECT
  segment,
  attribution_medium,
  attribution_source,
  attributed,
  city,
  country,
  distribution_id,
  first_seen_year,
  is_default_browser,
  channel,
  os,
  os_version,
  os_version_major,
  os_version_minor,
  submission_date,
  language_name,
  qdau as dau,
  wau,
  mau,
  new_profiles,
  ad_clicks,
  organic_search_count,
  search_count,
  search_with_ads,
  uri_count,
  active_hours,
  app_name,
  app_version,
  app_version_major,
  app_version_minor,
  app_version_patch_revision,
  app_version_is_major_release
FROM
  `moz-fx-data-shared-prod.firefox_desktop.active_users_aggregates`
