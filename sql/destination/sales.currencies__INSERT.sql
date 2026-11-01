INSERT INTO sales.currencies(
	currency_code, name, modified_date)	
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s);