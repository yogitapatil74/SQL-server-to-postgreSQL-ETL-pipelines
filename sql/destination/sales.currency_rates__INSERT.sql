INSERT INTO sales.currency_rates(
	currency_rate_id, currency_rate_date, from_currency_code, to_currency_code, average_rate, end_of_date_rate, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s);