CREATE TABLE IF NOT EXISTS sales.customers
(
    customer_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    person_id integer NULL DEFAULT NULL,
    store_id integer NULL DEFAULT NULL,
    sales_territory_id integer NULL DEFAULT NULL,
    account_number character varying(255) COLLATE pg_catalog."default" GENERATED ALWAYS AS (('SALES'::text || customer_id)) STORED,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_customers
        PRIMARY KEY (customer_id),
    CONSTRAINT fk_sales_customers_person_id
        FOREIGN KEY (person_id)
        REFERENCES people.people (person_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_sales_customers_sales_territory_id
        FOREIGN KEY (sales_territory_id)
        REFERENCES sales.sales_territories (sales_territory_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_sales_customers_store_id
        FOREIGN KEY (store_id)
        REFERENCES sales.stores (store_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_customers_customer_id
    ON sales.customers USING btree
    (customer_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_customers_person_id
    ON sales.customers USING btree
    (person_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_customers_store_id
    ON sales.customers USING btree
    (store_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_customers_sales_territory_id
    ON sales.customers USING btree
    (sales_territory_id ASC NULLS LAST)
    TABLESPACE pg_default;