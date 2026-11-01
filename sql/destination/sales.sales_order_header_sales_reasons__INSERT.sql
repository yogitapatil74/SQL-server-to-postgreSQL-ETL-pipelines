INSERT INTO sales.sales_order_header_sales_reasons(
	sales_order_id, sales_reason_id, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s);