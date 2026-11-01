CREATE TABLE IF NOT EXISTS sales.sales_territories_history
(
    sales_person_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    sales_territory_id integer NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL,
    CONSTRAINT pk_sales_territories_history
        PRIMARY KEY (sales_person_id, start_date, sales_territory_id),
    CONSTRAINT fk_sales_territories_history_sales_person_id
        FOREIGN KEY (sales_person_id)
        REFERENCES sales.sales_people (sales_person_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_sales_territories_history_sales_territory_id
        FOREIGN KEY (sales_territory_id)
        REFERENCES sales.sales_territories (sales_territory_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ck_sales_territories_history_end_date 
        CHECK (end_date >= start_date OR end_date IS NULL)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_territories_history
    ON sales.sales_territories_history USING btree
    (sales_person_id, start_date, sales_territory_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_territories_history_sales_person_id
    ON sales.sales_territories_history USING btree
    (sales_person_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_territories_history_start_date
    ON sales.sales_territories_history USING btree
    (start_date ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_territories_history_sales_territory_id
    ON sales.sales_territories_history USING btree
    (sales_territory_id ASC NULLS LAST)
    TABLESPACE pg_default;