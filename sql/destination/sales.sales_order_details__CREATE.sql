CREATE TABLE IF NOT EXISTS sales.sales_order_details
(
    sales_order_id integer NOT NULL,
    sales_order_detail_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    character_tracking_number character varying(25) COLLATE pg_catalog."default",
    order_quantity smallint NOT NULL,
    product_id integer NOT NULL,
    special_offer_id integer NOT NULL,
    unit_price decimal(18,2) NOT NULL DEFAULT 0.00,
    unit_price_discount decimal(18,2) NOT NULL,
    line_total decimal(18,2) GENERATED ALWAYS AS (COALESCE((unit_price*(1.00-unit_price_discount))*order_quantity,0.00)) STORED,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_sales_order_details
        PRIMARY KEY (sales_order_id, sales_order_detail_id),
    CONSTRAINT fk_sales_sales_order_details_sales_order_id
        FOREIGN KEY (sales_order_id)
        REFERENCES sales.sales_order_headers (sales_order_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_sales_sales_order_details_special_offer_products
        FOREIGN KEY (special_offer_id, product_id)
        REFERENCES sales.special_offer_products (special_offer_id, product_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ck_sales_sales_order_details_order_quantity 
        CHECK (order_quantity > 0),
    CONSTRAINT ck_sales_sales_order_details_unit_price 
        CHECK (unit_price >= 0.00),
    CONSTRAINT ck_sales_sales_order_details_unit_price_discount 
        CHECK (unit_price_discount >= 0.00)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_details
    ON sales.sales_order_details USING btree
    (sales_order_detail_id, sales_order_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_details_sales_order_detail_id
    ON sales.sales_order_details USING btree
    (sales_order_detail_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_details_sales_order_id
    ON sales.sales_order_details USING btree
    (sales_order_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_details_special_offer_products
    ON sales.sales_order_details USING btree
    (special_offer_id, product_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_details_product_id
    ON sales.sales_order_details USING btree
    (product_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_details_special_offer_id
    ON sales.sales_order_details USING btree
    (special_offer_id ASC NULLS LAST)
    TABLESPACE pg_default;