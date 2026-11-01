CREATE TABLE IF NOT EXISTS sales.currencies
(
    currency_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_currencies
        PRIMARY KEY (currency_code)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_currencies_currency_code
    ON sales.currencies USING btree
    (currency_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;