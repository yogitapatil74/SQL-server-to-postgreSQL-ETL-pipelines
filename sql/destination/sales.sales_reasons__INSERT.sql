INSERT INTO sales.sales_reasons(
	sales_reason_id, name, reason_type, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s);