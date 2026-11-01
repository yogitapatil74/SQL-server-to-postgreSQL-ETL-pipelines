CREATE TABLE IF NOT EXISTS people.email_addresses
(
    person_id integer NOT NULL,
    email_address_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    email_address character varying(50) COLLATE pg_catalog."default" NOT NULL,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_people_email_addresses
        PRIMARY KEY (person_id, email_address_id)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_email_addresses
    ON people.email_addresses USING btree
    (person_id, email_address_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_email_addresses_person_id
    ON people.email_addresses USING btree
    (person_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_email_addresses_email_address_id
    ON people.email_addresses USING btree
    (email_address_id ASC NULLS LAST)
    TABLESPACE pg_default;