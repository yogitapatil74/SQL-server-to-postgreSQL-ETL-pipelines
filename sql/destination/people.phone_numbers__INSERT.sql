INSERT INTO people.phone_numbers(
	person_id, phone_number, phone_number_type_id, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s);