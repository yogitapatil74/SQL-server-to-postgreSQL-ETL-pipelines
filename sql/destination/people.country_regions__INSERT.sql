INSERT INTO people.country_regions(
	country_region_code, name, modified_date) 
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s);