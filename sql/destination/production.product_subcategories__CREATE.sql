CREATE TABLE IF NOT EXISTS production.product_subcategories
(
    product_subcategory_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    product_category_id integer NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_production_product_subcategories
        PRIMARY KEY (product_subcategory_id),
    CONSTRAINT fk_production_product_subcategories_product_category_id 
        FOREIGN KEY (product_category_id)
        REFERENCES production.product_categories (product_category_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_production_product_subcategory_id
    ON production.product_subcategories USING btree
    (product_subcategory_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_production_product_category_id
    ON production.product_subcategories USING btree
    (product_category_id ASC NULLS LAST)
    TABLESPACE pg_default;