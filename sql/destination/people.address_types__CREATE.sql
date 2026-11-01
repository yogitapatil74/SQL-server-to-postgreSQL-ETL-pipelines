CREATE TABLE IF NOT EXISTS people.address_types
(
    address_type_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_people_address_types_id 
        PRIMARY KEY (address_type_id)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_address_types_address_type_id
    ON people.address_types USING btree
    (address_type_id ASC NULLS LAST)
    TABLESPACE pg_default;