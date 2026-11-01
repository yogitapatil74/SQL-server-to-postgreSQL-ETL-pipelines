INSERT INTO sales.customers(
	customer_id, person_id, store_id, sales_territory_id, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s);