CREATE TABLE IF NOT EXISTS
  `moz-fx-data-marketing-prod.acoustic.contact_v1`(
    email_id STRING,
    basket_token STRING,
    sfdc_id STRING,
    fxa_id STRING,
    double_opt_in BOOLEAN,
    has_opted_out_of_email BOOLEAN,
    email_lang STRING,
    email_format STRING,
    mailing_country STRING,
    cohort STRING,
    fxa_created_date DATE,
    fxa_first_service STRING,
    fxa_account_deleted BOOLEAN,
    sub_common_voice BOOLEAN,
    sub_firefox_accounts_journey BOOLEAN,
    sub_firefox_news BOOLEAN,
    sub_hubs BOOLEAN,
    sub_internet_health_report BOOLEAN,
    sub_knowledge_is_power BOOLEAN,
    sub_miti BOOLEAN,
    sub_mixed_reality BOOLEAN,
    sub_mozilla_fellowship_awardee_alumni BOOLEAN,
    sub_mozilla_festival BOOLEAN,
    sub_mozilla_foundation BOOLEAN,
    sub_mozilla_technology BOOLEAN,
    sub_mozillians_nda BOOLEAN,
    sub_take_action_for_the_internet BOOLEAN,
    sub_test_pilot BOOLEAN,
    sub_about_mozilla BOOLEAN,
    sub_apps_and_hacks BOOLEAN,
    sub_rally BOOLEAN,
    sub_firefox_sweepstakes BOOLEAN,
    vpn_waitlist_geo STRING,
    vpn_waitlist_platform ARRAY<STRING>,
    relay_waitlist_geo STRING,
    recipient_id INTEGER,
    date_created DATE,
    last_modified_date DATE
  )
PARTITION BY
  last_modified_date
CLUSTER BY
  has_opted_out_of_email,
  double_opt_in,
  email_lang,
  mailing_country
