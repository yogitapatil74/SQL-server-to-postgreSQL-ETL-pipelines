CREATE TABLE IF NOT EXISTS people.phone_number_types
(
    phone_number_type_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_people_phone_number_types
        PRIMARY KEY (phone_number_type_id)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_phone_number_types_phone_number_type_id
    ON people.phone_number_types USING btree
    (phone_number_type_id ASC NULLS LAST)
    TABLESPACE pg_default;