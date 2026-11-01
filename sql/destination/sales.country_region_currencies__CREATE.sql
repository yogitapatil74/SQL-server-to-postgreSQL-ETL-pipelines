CREATE TABLE IF NOT EXISTS sales.country_region_currencies
(
    country_region_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    currency_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_country_region_currencies 
        PRIMARY KEY (country_region_code, currency_code),
    CONSTRAINT fk_sales_country_region_currencies_country_region_code
        FOREIGN KEY (country_region_code)
        REFERENCES people.country_regions (country_region_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_sales_country_region_currencies_currency_code
        FOREIGN KEY (currency_code)
        REFERENCES sales.currencies (currency_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_country_region_currencies
    ON sales.country_region_currencies USING btree
    (country_region_code, currency_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_country_region_currencies_country_region_code
    ON sales.country_region_currencies USING btree
    (country_region_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_country_region_currencies_currency_code
    ON sales.country_region_currencies USING btree
    (currency_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;