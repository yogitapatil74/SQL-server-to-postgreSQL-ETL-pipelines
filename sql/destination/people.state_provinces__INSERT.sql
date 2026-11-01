INSERT INTO people.state_provinces(
	state_province_id, state_province_code, country_region_code, is_only_state_province_flag, name, sales_territory_id, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s, %s);