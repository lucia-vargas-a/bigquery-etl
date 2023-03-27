SELECT
  id,
  _fivetran_synced,
  amount,
  balance_transaction_id,
  charge_id,
  connected_account_id,
  created,
  currency,
  description,
  failure_balance_transaction_id,
  failure_reason,
  metadata,
  payment_intent_id,
  reason,
  receipt_number,
  status,
FROM
  `dev-fivetran`.stripe_nonprod.refund
