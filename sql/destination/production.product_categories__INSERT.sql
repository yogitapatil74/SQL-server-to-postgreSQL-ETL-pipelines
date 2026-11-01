INSERT INTO production.product_categories(
	product_category_id, name, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s);