INSERT INTO sales.sales_people_quota_history(
	sales_person_id, quota_date, sales_quota, rowguid, modified_date)
 OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s, %s);