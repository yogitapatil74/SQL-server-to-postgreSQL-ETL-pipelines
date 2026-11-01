CREATE TABLE IF NOT EXISTS people.state_provinces
(
    state_province_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    state_province_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    country_region_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    is_only_state_province_flag boolean NOT NULL DEFAULT TRUE,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    sales_territory_id integer NOT NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_people_state_provinces PRIMARY KEY (state_province_id),
    CONSTRAINT fk_people_state_provinces_country_region_code FOREIGN KEY (country_region_code)
        REFERENCES people.country_regions (country_region_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT fk_people_state_provinces_sales_territory_id FOREIGN KEY (sales_territory_id)
        REFERENCES sales.sales_territories (sales_territory_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_tax_rates_state_province_id
    ON people.state_provinces USING btree
    (state_province_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_state_provinces_country_region_code
    ON people.state_provinces USING btree
    (country_region_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_state_provinces_sales_territory_id
    ON people.state_provinces USING btree
    (sales_territory_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_state_provinces_is_only_state_province_flag_false
    ON people.state_provinces USING btree
    (is_only_state_province_flag ASC NULLS LAST)
    TABLESPACE pg_default
    WHERE is_only_state_province_flag = FALSE;

CREATE INDEX IF NOT EXISTS idx_people_state_provinces_is_only_state_province_flag_true
    ON people.state_provinces USING btree
    (is_only_state_province_flag ASC NULLS LAST)
    TABLESPACE pg_default
    WHERE is_only_state_province_flag = TRUE;