INSERT INTO sales.sales_territories(
	sales_territory_id, name, country_region_code, region, sales_ytd, sales_last_year, cost_ytd, cost_last_year, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);