CREATE TABLE IF NOT EXISTS production.products
(
    product_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    product_number character varying(25) COLLATE pg_catalog."default" NOT NULL,
    make_flag bit(1) NOT NULL DEFAULT '1'::"bit",
    finished_goods bit(1) NOT NULL DEFAULT '1'::"bit",
    color character varying(15) COLLATE pg_catalog."default",
    safety_stock_level smallint NOT NULL,
    reorder_point smallint NOT NULL,
    standard_cost numeric(18,2) NOT NULL DEFAULT 0,
    list_price numeric(18,2) NOT NULL DEFAULT 0,
    size character varying(5) COLLATE pg_catalog."default",
    size_unit_measure_code character varying(3) COLLATE pg_catalog."default",
    weight_unit_measure_code character varying(3) COLLATE pg_catalog."default",
    weight numeric(8,2) NULL DEFAULT 0,
    days_to_manufacture integer NOT NULL,
    product_line character varying(2) COLLATE pg_catalog."default",
    class character varying(2) COLLATE pg_catalog."default",
    style character varying(2) COLLATE pg_catalog."default",
    product_subcategory_id integer,
    product_model_id integer,
    sell_start_date timestamp without time zone NOT NULL,
    sell_end_date timestamp without time zone,
    discontinued_date timestamp without time zone,
    rowguid uuid NOT NULL DEFAULT gen_random_uuid(),
    modified_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_production_products PRIMARY KEY (product_id),
    CONSTRAINT fk_production_products_product_model_id FOREIGN KEY (product_model_id)
        REFERENCES production.product_models (product_model_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_production_products_product_subcategory_id FOREIGN KEY (product_subcategory_id)
        REFERENCES production.product_subcategories (product_subcategory_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_production_products_size_unit_measure_code FOREIGN KEY (size_unit_measure_code)
        REFERENCES production.unit_measures (unit_measure_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_production_products_weight_unit_measure_code FOREIGN KEY (weight_unit_measure_code)
        REFERENCES production.unit_measures (unit_measure_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ck_production_products_class CHECK ((upper(class::text) = ANY (ARRAY['H'::text, 'L'::text, 'M'::text])) OR class IS NULL),
    CONSTRAINT ck_production_products_days_to_manufacture CHECK (days_to_manufacture >= 0),
    CONSTRAINT ck_production_products_list_price CHECK (list_price >= 0.00),
    CONSTRAINT ck_production_products_product_line CHECK ((upper(product_line::text) = ANY (ARRAY['R'::text, 'M'::text, 'T'::text, 'S'::text])) OR product_line IS NULL),
    CONSTRAINT ck_production_products_reorder_point CHECK (reorder_point >= 0),
    CONSTRAINT ck_production_products_safety_stock_level CHECK (safety_stock_level >= 0),
    CONSTRAINT ck_production_products_sell_end_date CHECK (sell_end_date >= sell_start_date OR sell_end_date IS NULL),
    CONSTRAINT ck_production_products_standard_cost CHECK (standard_cost >= 0.00),
    CONSTRAINT ck_production_products_style CHECK ((upper(style::text) = ANY (ARRAY['U'::text, 'M'::text, 'W'::text])) OR style IS NULL),
    CONSTRAINT ck_production_products_weight CHECK (weight > 0.00)
)

TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_production_products_finished_goods_false
    ON production.products USING btree
    (finished_goods ASC NULLS LAST)
    TABLESPACE pg_default
    WHERE finished_goods = '0'::"bit";

CREATE INDEX IF NOT EXISTS idx_production_products_finished_goods_true
    ON production.products USING btree
    (finished_goods ASC NULLS LAST)
    TABLESPACE pg_default
    WHERE finished_goods = '1'::"bit";

CREATE INDEX IF NOT EXISTS idx_production_products_make_flag_false
    ON production.products USING btree
    (make_flag ASC NULLS LAST)
    TABLESPACE pg_default
    WHERE make_flag = '0'::"bit";

CREATE INDEX IF NOT EXISTS idx_production_products_make_flag_true
    ON production.products USING btree
    (make_flag ASC NULLS LAST)
    TABLESPACE pg_default
    WHERE make_flag = '1'::"bit";

CREATE INDEX IF NOT EXISTS idx_production_products_size_unit_measure_code
    ON production.products USING btree
    (size_unit_measure_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_production_products_weight_unit_measure_code
    ON production.products USING btree
    (weight_unit_measure_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;