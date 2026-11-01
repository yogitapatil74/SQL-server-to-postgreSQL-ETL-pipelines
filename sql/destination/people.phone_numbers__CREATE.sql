CREATE TABLE IF NOT EXISTS people.phone_numbers
(
    person_id integer NOT NULL,
    phone_number character varying(25) COLLATE pg_catalog."default" NOT NULL,
    phone_number_type_id integer NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_people_phone_numbers 
        PRIMARY KEY (person_id, phone_number, phone_number_type_id),
    CONSTRAINT fk_people_phone_numbers_person_id
        FOREIGN KEY (person_id)
        REFERENCES people.people (person_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT fk_people_phone_numbers_phone_number_type_id
        FOREIGN KEY (phone_number_type_id)
        REFERENCES people.phone_number_types (phone_number_type_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_phone_numbers
    ON people.phone_numbers USING btree
    (person_id, phone_number, phone_number_type_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_phone_numbers_person_id
    ON people.phone_numbers USING btree
    (person_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_phone_numbers_phone_number_type_id
    ON people.phone_numbers USING btree
    (phone_number_type_id ASC NULLS LAST)
    TABLESPACE pg_default;