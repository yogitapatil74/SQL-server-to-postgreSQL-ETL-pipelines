CREATE TABLE IF NOT EXISTS people.country_regions
(
    country_region_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_people_country_regions 
        PRIMARY KEY (country_region_code)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_country_regions_country_region_code
    ON people.country_regions USING btree
    (country_region_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;