CREATE TABLE IF NOT EXISTS sales.special_offer_products
(
    special_offer_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    product_id integer NOT NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_special_offer_products
        PRIMARY KEY (special_offer_id, product_id),
    CONSTRAINT fk_special_offer_products_product_id
        FOREIGN KEY (product_id)
        REFERENCES production.products (product_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_special_offer_special_offer_id
        FOREIGN KEY (special_offer_id)
        REFERENCES sales.special_offers (special_offer_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_special_offer_products
    ON sales.special_offer_products USING btree
    (special_offer_id, product_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_special_offer_products_special_offer_id
    ON sales.special_offer_products USING btree
    (special_offer_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_special_offer_products_product_id
    ON sales.special_offer_products USING btree
    (product_id ASC NULLS LAST)
    TABLESPACE pg_default;