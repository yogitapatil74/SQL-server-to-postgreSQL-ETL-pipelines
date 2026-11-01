INSERT INTO production.product_descriptions(
	product_description_id, description, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s);