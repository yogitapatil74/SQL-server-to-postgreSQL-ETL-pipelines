CREATE TABLE IF NOT EXISTS sales.credit_cards
(
    credit_card_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    card_type character varying(50) COLLATE pg_catalog."default" NOT NULL,
    card_number character varying(25) COLLATE pg_catalog."default" NOT NULL,
    exp_month smallint NOT NULL,
    exp_year smallint NOT NULL,
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sales_credit_cards 
        PRIMARY KEY (credit_card_id)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_credit_cards_credit_card_id
    ON sales.credit_cards USING btree
    (credit_card_id ASC NULLS LAST)
    TABLESPACE pg_default;