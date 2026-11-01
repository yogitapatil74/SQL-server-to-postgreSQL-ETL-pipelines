INSERT INTO sales.sales_territories_history(
	sales_person_id, sales_territory_id, start_date, end_date, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s);