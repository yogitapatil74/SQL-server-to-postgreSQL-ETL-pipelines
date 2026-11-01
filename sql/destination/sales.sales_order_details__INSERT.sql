INSERT INTO sales.sales_order_details(
	sales_order_id, sales_order_detail_id, character_tracking_number, order_quantity, product_id, special_offer_id, unit_price, unit_price_discount, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);