CREATE TABLE IF NOT EXISTS sales.sales_reasons
(
    sales_reason_id integer NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    reason_type character varying(50) COLLATE pg_catalog."default" NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_sales_reasons
        PRIMARY KEY (sales_reason_id)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_reasons_sales_reason_id
    ON sales.sales_reasons USING btree
    (sales_reason_id ASC NULLS LAST)
    TABLESPACE pg_default;