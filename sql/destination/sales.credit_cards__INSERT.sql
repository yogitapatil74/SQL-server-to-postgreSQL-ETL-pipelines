INSERT INTO sales.credit_cards(
	credit_card_id, card_type, card_number, exp_month, exp_year, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s, %s);