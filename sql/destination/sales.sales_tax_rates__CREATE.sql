CREATE TABLE IF NOT EXISTS sales.sales_tax_rates
(
    sales_tax_rate_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    state_province_id integer NOT NULL,
    tax_type smallint NOT NULL,
    tax_rate decimal(18,2) NOT NULL DEFAULT 0.00,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_sales_tax_rates
        PRIMARY KEY (sales_tax_rate_id),
    CONSTRAINT fk_sales_sales_tax_rates_state_province_id
        FOREIGN KEY (state_province_id)
        REFERENCES people.state_provinces (state_province_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ck_sales_sales_tax_rates_tax_type
        CHECK (tax_type >= 1 AND tax_type <= 3)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_tax_rates_sales_tax_rate_id
    ON sales.sales_tax_rates USING btree
    (sales_tax_rate_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_tax_rates_state_province_id
    ON sales.sales_tax_rates USING btree
    (state_province_id ASC NULLS LAST)
    TABLESPACE pg_default;