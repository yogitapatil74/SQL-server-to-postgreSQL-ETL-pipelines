CREATE TABLE IF NOT EXISTS sales.sales_territories
(
    sales_territory_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    country_region_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    region character varying(50) COLLATE pg_catalog."default" NOT NULL,
    sales_ytd decimal(18,2) NOT NULL DEFAULT 0.00,
    sales_last_year decimal(18,2) NOT NULL DEFAULT 0.00,
    cost_ytd decimal(18,2) NOT NULL DEFAULT 0.00,
    cost_last_year decimal(18,2) NOT NULL DEFAULT 0.00,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_sales_territories
        PRIMARY KEY (sales_territory_id),
    CONSTRAINT fk_sales_sales_territories_country_region_code
        FOREIGN KEY (country_region_code)
        REFERENCES people.country_regions (country_region_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_territories_sales_territory_id
    ON sales.sales_territories USING btree
    (sales_territory_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_territories_country_region_code
    ON sales.sales_territories USING btree
    (country_region_code ASC NULLS LAST)
    TABLESPACE pg_default;