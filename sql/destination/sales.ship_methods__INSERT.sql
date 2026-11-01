INSERT INTO sales.ship_methods(
	ship_method_id, name, ship_base, ship_rate, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s);