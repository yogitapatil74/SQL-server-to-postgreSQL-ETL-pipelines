INSERT INTO production.product_models(
	product_model_id, name, catalog_description, instructions, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s);