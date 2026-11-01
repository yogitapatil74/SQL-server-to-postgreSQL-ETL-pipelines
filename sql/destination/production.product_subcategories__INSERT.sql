INSERT INTO production.product_subcategories(
	product_subcategory_id, product_category_id, name, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s);