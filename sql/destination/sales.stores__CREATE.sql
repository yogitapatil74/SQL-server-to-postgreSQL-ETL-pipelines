CREATE TABLE IF NOT EXISTS sales.stores
(
    store_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    sales_person_id integer NOT NULL,
    demographics text COLLATE pg_catalog."default" NOT NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_stores
        PRIMARY KEY (store_id),
    CONSTRAINT fk_sales_stores_sales_person_id 
        FOREIGN KEY (sales_person_id)
        REFERENCES sales.sales_people (sales_person_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_store_store_id
    ON sales.stores USING btree
    (store_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_store_sales_person_id
    ON sales.stores USING btree
    (sales_person_id ASC NULLS LAST)
    TABLESPACE pg_default;