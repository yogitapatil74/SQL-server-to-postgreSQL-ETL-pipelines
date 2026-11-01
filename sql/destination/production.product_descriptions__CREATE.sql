CREATE TABLE IF NOT EXISTS production.product_descriptions
(
    product_description_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    description character varying COLLATE pg_catalog."default" NOT NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_production_product_descriptions
        PRIMARY KEY (product_description_id)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_production_product_descriptions_product_description_id
    ON production.product_descriptions USING btree
    (product_description_id ASC NULLS LAST)
    TABLESPACE pg_default;