INSERT INTO people.phone_number_types(
	phone_number_type_id, name, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s);