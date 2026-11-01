INSERT INTO people.locations(
	city_name, state_province_code, state_province_name, country_region_code, country_region_name, region, sub_region, latitude,longitude,rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);