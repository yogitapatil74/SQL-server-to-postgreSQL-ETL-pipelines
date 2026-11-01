INSERT INTO people.address_types(
	address_type_id, name, rowguid, modified_date) 
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s);