INSERT INTO sales.shopping_cart_items(
	shopping_cart_item_id, shopping_cart_id, quantity, product_id, date_created, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s);