INSERT INTO sales.sales_people(
	sales_person_id, sales_territory_id, sales_quota, bonus, commission_pct, sales_ytd, sales_last_year, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);