INSERT INTO sales.country_region_currencies(
	country_region_code, currency_code, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s);