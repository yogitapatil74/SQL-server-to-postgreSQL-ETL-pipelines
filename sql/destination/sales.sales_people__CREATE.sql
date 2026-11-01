CREATE TABLE IF NOT EXISTS sales.sales_people
(
    sales_person_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    sales_territory_id integer,
    sales_quota decimal(18,2) DEFAULT 0.00,
    bonus decimal(18,2) DEFAULT 0.00,
    commission_pct decimal(18,2) DEFAULT 0.00,
    sales_ytd decimal(18,2) DEFAULT 0.00,
    sales_last_year decimal(18,2) DEFAULT 0.00,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_sales_people
        PRIMARY KEY (sales_person_id),
    CONSTRAINT fk_sales_sales_people_sales_territory_id
        FOREIGN KEY (sales_territory_id)
        REFERENCES sales.sales_territories (sales_territory_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ck_sales_sales_people_commission_pct 
        CHECK (commission_pct >= '0.00'),
    CONSTRAINT ck_sales_sales_people_sales_quota 
        CHECK (sales_quota >= '0.00'),
    CONSTRAINT ck_sales_sales_people_bonus 
        CHECK (bonus >= '0.00'),
    CONSTRAINT ck_sales_sales_people_sales_ytd 
        CHECK (sales_ytd >= '0.00'),
    CONSTRAINT ck_sales_sales_people_sales_last_year 
        CHECK (sales_last_year >= '0.00')
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_people_sales_person_id
    ON sales.sales_people USING btree
    (sales_person_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_people_sales_territory_id
    ON sales.sales_people USING btree
    (sales_territory_id ASC NULLS LAST)
    TABLESPACE pg_default;