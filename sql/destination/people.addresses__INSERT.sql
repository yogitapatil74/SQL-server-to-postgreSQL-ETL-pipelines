INSERT INTO people.addresses(
	address_id, address_line1, address_line2, city, state_province_id, postal_code, spatial_location, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);