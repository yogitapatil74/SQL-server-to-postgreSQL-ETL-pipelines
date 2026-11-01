INSERT INTO people.email_addresses(
	person_id, email_address_id, email_address, rowguid, modified_date) 
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s);