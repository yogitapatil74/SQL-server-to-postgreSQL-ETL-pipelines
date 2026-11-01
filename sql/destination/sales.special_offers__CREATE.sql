CREATE TABLE IF NOT EXISTS sales.special_offers
(
    special_offer_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    description character varying(255) COLLATE pg_catalog."default" NOT NULL,
    discount_pct decimal(18,2) NOT NULL DEFAULT 0.00,
    type character varying(50) COLLATE pg_catalog."default" NOT NULL,
    category character varying(50) COLLATE pg_catalog."default" NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    min_qty integer NOT NULL DEFAULT 0,
    max_qty integer NULL DEFAULT 0,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_special_offers
        PRIMARY KEY (special_offer_id),
    CONSTRAINT ck_discount_pct CHECK (discount_pct >= 0.00),
    CONSTRAINT ck_end_date CHECK (end_date >= start_date),
    CONSTRAINT ck_max_qty CHECK (max_qty >= 0),
    CONSTRAINT ck_min_qty CHECK (min_qty >= 0)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_special_offers_special_offer_id
    ON sales.special_offers USING btree
    (special_offer_id ASC NULLS LAST)
    TABLESPACE pg_default;