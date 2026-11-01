INSERT INTO sales.sales_person_credit_cards(
	sales_person_id, credit_card_id, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s);