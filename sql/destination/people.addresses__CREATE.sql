CREATE TABLE IF NOT EXISTS people.addresses
(
    address_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    address_line1 character varying(60) COLLATE pg_catalog."default" NOT NULL,
    address_line2 character varying(60) COLLATE pg_catalog."default" NULL,
    city character varying(30) COLLATE pg_catalog."default" NOT NULL,
    state_province_id integer NOT NULL,
    postal_code character varying(15) COLLATE pg_catalog."default" NOT NULL,
    spatial_location text COLLATE pg_catalog."default",
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_people_addresses 
        PRIMARY KEY (address_id),
    CONSTRAINT fk_people_addresses_state_province_id
        FOREIGN KEY (state_province_id)
        REFERENCES people.state_provinces (state_province_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_addresses_address_id
    ON people.addresses USING btree
    (address_id ASC NULLS LAST)
    TABLESPACE pg_default;
	
CREATE INDEX IF NOT EXISTS idx_people_addresses_state_province_id
    ON people.addresses USING btree
    (state_province_id ASC NULLS LAST)
    TABLESPACE pg_default;