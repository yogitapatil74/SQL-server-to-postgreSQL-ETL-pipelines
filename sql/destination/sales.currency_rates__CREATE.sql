CREATE TABLE IF NOT EXISTS sales.currency_rates
(
    currency_rate_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    currency_rate_date timestamp without time zone NOT NULL,
    from_currency_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    to_currency_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    average_rate decimal(18,2) NOT NULL,
    end_of_date_rate decimal(18,2) NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_currency_rates
        PRIMARY KEY (currency_rate_id),
    CONSTRAINT fk_sales_currency_rates_from_currency_code 
        FOREIGN KEY (from_currency_code)
        REFERENCES sales.currencies (currency_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_sales_currency_rates_to_currency_code
        FOREIGN KEY (to_currency_code)
        REFERENCES sales.currencies (currency_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_currency_rates_currency_rate_id
    ON sales.currency_rates USING btree
    (currency_rate_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_currency_rates_from_currency_code
    ON sales.currency_rates USING btree
    (from_currency_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_currency_rates_to_currency_code
    ON sales.currency_rates USING btree
    (to_currency_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;