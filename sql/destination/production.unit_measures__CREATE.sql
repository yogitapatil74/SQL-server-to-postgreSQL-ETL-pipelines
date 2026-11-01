CREATE TABLE IF NOT EXISTS production.unit_measures
(
    unit_measure_code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_production_unit_measures 
        PRIMARY KEY (unit_measure_code)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_production_unit_measures_measure_code
    ON production.unit_measures USING btree
    (unit_measure_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;