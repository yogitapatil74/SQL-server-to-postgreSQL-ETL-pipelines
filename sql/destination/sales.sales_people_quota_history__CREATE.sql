CREATE TABLE IF NOT EXISTS sales.sales_people_quota_history
(
    sales_person_id integer NOT NULL,
    quota_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sales_quota decimal(18,2) NOT NULL DEFAULT 0.00,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_sales_person_quota_history
        PRIMARY KEY (sales_person_id, quota_date),
    CONSTRAINT fk_sales_sales_person_quota_history_sales_person_id
        FOREIGN KEY (sales_person_id)
        REFERENCES sales.sales_people (sales_person_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ck_sales_sales_people_quota_history_sales_quota 
        CHECK (sales_quota >= '0.00')
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_people_quota_history
    ON sales.sales_people_quota_history USING btree
    (sales_person_id, quota_date)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_people_quota_history_sales_person_id
    ON sales.sales_people_quota_history USING btree
    (sales_person_id ASC NULLS LAST)
    TABLESPACE pg_default;