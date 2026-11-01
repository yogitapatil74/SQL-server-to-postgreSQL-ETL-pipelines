CREATE TABLE IF NOT EXISTS sales.sales_person_credit_cards
(
    sales_person_id integer NOT NULL,
    credit_card_id integer NOT NULL,
    modified_date timestamp without time zone NOT NULL,
    CONSTRAINT pk_sales_person_credit_cards
        PRIMARY KEY (sales_person_id, credit_card_id),
    CONSTRAINT fk_sales_person_credit_cards_credit_card_id
        FOREIGN KEY (credit_card_id)
        REFERENCES sales.credit_cards (credit_card_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_person_credit_cards
    ON sales.sales_person_credit_cards USING btree
    (sales_person_id, credit_card_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_person_credit_cards_sales_person_id
    ON sales.sales_person_credit_cards USING btree
    (sales_person_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_sales_sales_person_credit_cards_credit_card_id
    ON sales.sales_person_credit_cards USING btree
    (credit_card_id ASC NULLS LAST)
    TABLESPACE pg_default;