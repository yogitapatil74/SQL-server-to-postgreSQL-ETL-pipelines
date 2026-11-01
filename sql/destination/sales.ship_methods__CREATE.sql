CREATE TABLE IF NOT EXISTS sales.ship_methods
(
    ship_method_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    ship_base decimal(18,2) NOT NULL DEFAULT 0.00,
    ship_rate decimal(18,2) NOT NULL DEFAULT 0.00,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_ship_methods
        PRIMARY KEY (ship_method_id),
    CONSTRAINT ck_sales_ship_methods_ship_base
        CHECK (ship_base >= '0.00'),
    CONSTRAINT ck_sales_ship_methods_ship_rate
        CHECK (ship_rate >= '0.00')
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_ship_methods_ship_method_id
    ON sales.ship_methods USING btree
    (ship_method_id ASC NULLS LAST)
    TABLESPACE pg_default;