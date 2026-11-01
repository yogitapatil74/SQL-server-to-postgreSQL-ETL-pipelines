CREATE TABLE IF NOT EXISTS sales.shopping_cart_items
(
    shopping_cart_item_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    shopping_cart_id integer NOT NULL,
    quantity integer NOT NULL DEFAULT 1,
    product_id integer NOT NULL,
    date_created timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_shopping_cart_items
        PRIMARY KEY (shopping_cart_item_id),
    CONSTRAINT fk_sales_shopping_cart_items_product_id
        FOREIGN KEY (product_id)
        REFERENCES production.products (product_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ck_sales_shopping_cart_items_quantity
        CHECK (quantity >= 1)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_shopping_cart_items_shopping_card_id
    ON sales.shopping_cart_items USING btree
    (shopping_cart_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_shopping_cart_items_product_id
    ON sales.shopping_cart_items USING btree
    (product_id ASC NULLS LAST)
    TABLESPACE pg_default;