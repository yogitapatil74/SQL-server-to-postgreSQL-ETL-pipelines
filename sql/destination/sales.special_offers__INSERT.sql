INSERT INTO sales.special_offers(
	special_offer_id, description, discount_pct, type, category, start_date, end_date, min_qty, max_qty, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);