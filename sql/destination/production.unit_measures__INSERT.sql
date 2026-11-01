INSERT INTO production.unit_measures(
	unit_measure_code, name, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s);