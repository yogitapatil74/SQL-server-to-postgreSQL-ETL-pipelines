CREATE TABLE IF NOT EXISTS sales.sales_order_headers
(
    sales_order_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    revision_number smallint NOT NULL DEFAULT 0,
    order_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ship_date timestamp without time zone NULL,
    status smallint NOT NULL DEFAULT 1,
    online_order_flag bit(1) NOT NULL DEFAULT '1'::"bit",
    sales_order_number character varying(255) COLLATE pg_catalog."default" GENERATED ALWAYS AS (COALESCE('SO' || sales_order_id::VARCHAR,'*** ERROR ***')) STORED,
    purchase_order_number character varying(255) COLLATE pg_catalog."default",
    account_number character varying(255) COLLATE pg_catalog."default",
    customer_id integer NOT NULL,
    sales_person_id integer NULL,
    sales_territory_id integer NULL,
    bill_to_address_id integer NOT NULL,
    ship_to_address_id integer NOT NULL,
    ship_method_id integer NOT NULL,
    credit_card_id integer NULL,
    credit_card_approval_code character varying(15) COLLATE pg_catalog."default" NULL,
    currency_rate_id integer NULL,
    subtotal decimal(18,2) NOT NULL DEFAULT 0.00,
    tax_amount decimal(18,2) NOT NULL DEFAULT 0.00,
    freight decimal(18,2) NOT NULL DEFAULT 0.00,
    comment character varying(128) COLLATE pg_catalog."default",
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_sales_order_headers
        PRIMARY KEY (sales_order_id),
    CONSTRAINT fk_sales_sales_order_headers_bill_to_address_id
        FOREIGN KEY (bill_to_address_id)
        REFERENCES people.addresses (address_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT fk_sales_sales_order_headers_credit_card_id
        FOREIGN KEY (credit_card_id)
        REFERENCES sales.credit_cards (credit_card_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT fk_sales_sales_order_headers_currency_rate_id
        FOREIGN KEY (currency_rate_id)
        REFERENCES sales.currency_rates (currency_rate_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT fk_sales_sales_order_headers_customer_id
        FOREIGN KEY (customer_id)
        REFERENCES sales.customers (customer_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT fk_sales_sales_order_headers_sales_person_id
        FOREIGN KEY (sales_person_id)
        REFERENCES sales.sales_people (sales_person_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT fk_sales_sales_order_headers_sales_territory_id
        FOREIGN KEY (sales_territory_id)
        REFERENCES sales.sales_territories (sales_territory_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT fk_sales_sales_order_headers_ship_method_id
        FOREIGN KEY (ship_method_id)
        REFERENCES sales.ship_methods (ship_method_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT fk_sales_sales_order_headers_ship_to_address_id
        FOREIGN KEY (ship_to_address_id)
        REFERENCES people.addresses (address_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT ck_sales_sales_order_headers_freight 
        CHECK (freight >= '0.00'),
    CONSTRAINT ck_sales_sales_order_headers_subtotal 
        CHECK (subtotal >= '0.00'),
    CONSTRAINT ck_sales_sales_order_headers_tax_amount 
        CHECK (tax_amount >= '0.00'),
    CONSTRAINT ck_sales_sales_order_headers_due_date 
        CHECK (due_date >= order_date),
    CONSTRAINT ck_sales_sales_order_headers_ship_date 
        CHECK (ship_date >= order_date OR ship_date IS NULL),
    CONSTRAINT ck_sales_sales_order_headers_status 
        CHECK (status >= 0 AND status <= 8)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_sales_order_id
    ON sales.sales_order_headers USING btree
    (sales_order_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_customer_id
    ON sales.sales_order_headers USING btree
    (customer_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_sales_person_id
    ON sales.sales_order_headers USING btree
    (sales_person_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_sales_territory_id
    ON sales.sales_order_headers USING btree
    (sales_territory_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_bill_to_address_id
    ON sales.sales_order_headers USING btree
    (bill_to_address_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_ship_to_address_id
    ON sales.sales_order_headers USING btree
    (ship_to_address_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_ship_method_id
    ON sales.sales_order_headers USING btree
    (ship_method_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_credit_card_id
    ON sales.sales_order_headers USING btree
    (credit_card_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_currency_rate_id
    ON sales.sales_order_headers USING btree
    (currency_rate_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_online_order_flag_true
    ON sales.sales_order_headers USING btree
    (online_order_flag ASC NULLS LAST)
    WHERE online_order_flag = B'1';

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_headers_online_order_flag_false
    ON sales.sales_order_headers USING btree
    (online_order_flag ASC NULLS LAST)
    WHERE online_order_flag = B'0';