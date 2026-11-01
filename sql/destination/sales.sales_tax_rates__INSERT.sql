INSERT INTO sales.sales_tax_rates(
	sales_tax_rate_id, state_province_id, tax_type, tax_rate, name, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s);