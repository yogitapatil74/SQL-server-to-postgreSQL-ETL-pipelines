CREATE TABLE IF NOT EXISTS sales.sales_order_header_sales_reasons
(
    sales_order_id integer NOT NULL,
    sales_reason_id integer NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_sales_order_header_sales_reasons
        PRIMARY KEY (sales_order_id, sales_reason_id),
    CONSTRAINT fk_sales_sales_order_header_sales_reasons_sales_order_id
        FOREIGN KEY (sales_order_id)
        REFERENCES sales.sales_order_headers (sales_order_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_sales_sales_order_header_sales_reasons_sales_reason_id
        FOREIGN KEY (sales_reason_id)
        REFERENCES sales.sales_reasons (sales_reason_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_header_sales_reasons
    ON sales.sales_order_header_sales_reasons USING btree
    (sales_order_id, sales_reason_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_header_sales_reasons_sales_order_id
    ON sales.sales_order_header_sales_reasons USING btree
    (sales_order_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_order_header_sales_reasons_sales_reason_id
    ON sales.sales_order_header_sales_reasons USING btree
    (sales_reason_id ASC NULLS LAST)
    TABLESPACE pg_default;