INSERT INTO sales.stores(
	store_id, name, sales_person_id, demographics, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s);