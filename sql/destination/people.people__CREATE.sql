CREATE TABLE IF NOT EXISTS people.people
(
    person_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    person_type character varying(2) COLLATE pg_catalog."default" NOT NULL,
    name_style boolean NOT NULL DEFAULT false,
    title character varying(8) NULL COLLATE pg_catalog."default",
    first_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    middle_name character varying(50) NULL COLLATE pg_catalog."default",
    last_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    suffix character varying(10) NULL COLLATE pg_catalog."default",
    email_promotion integer NOT NULL DEFAULT 0,
    additional_contact_info text COLLATE pg_catalog."default",
    demographics text COLLATE pg_catalog."default",
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_people_person
        PRIMARY KEY (person_id),
    CONSTRAINT ck_people_person_email_promotion
        CHECK (email_promotion >= 0 AND email_promotion <= 2),
    CONSTRAINT ck_people_person_person_type 
        CHECK (person_type IS NULL OR (UPPER(person_type) IN('GC','SP','EM','IN','VC','SC')))
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_people_person_id
    ON people.people USING btree
    (person_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_people_person_type
    ON people.people USING btree
    (person_type ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_people_people_email_promotion
    ON people.people USING btree
    (email_promotion ASC NULLS LAST)
    TABLESPACE pg_default;