INSERT INTO sales.special_offer_products(
	special_offer_id, product_id, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s);