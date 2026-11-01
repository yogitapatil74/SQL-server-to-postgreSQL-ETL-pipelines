CREATE TABLE IF NOT EXISTS people.locations
(
	location_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    city_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    state_province_code character varying(5) COLLATE pg_catalog."default" NOT NULL,
    state_province_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    country_region_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    country_region_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    region character varying(255) COLLATE pg_catalog."default" NOT NULL,
    sub_region character varying(255) COLLATE pg_catalog."default" NOT NULL,
    latitude numeric(14,11) NULL,
    longitude numeric(14,11) NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_people_locations PRIMARY KEY (location_id)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_locations_location_id
    ON people.locations USING btree
    (location_id ASC NULLS LAST)
    TABLESPACE pg_default;