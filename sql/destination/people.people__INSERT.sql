INSERT INTO people.people(
	person_id, person_type, name_style, title, first_name, middle_name, last_name, suffix, email_promotion, additional_contact_info, demographics, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);