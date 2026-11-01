CREATE TABLE IF NOT EXISTS production.product_categories
(
    product_category_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_production_product_categories
        PRIMARY KEY (product_category_id)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_production_product_categories_product_category_id
    ON production.product_categories USING btree
    (product_category_id ASC NULLS LAST)
    TABLESPACE pg_default;