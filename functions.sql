-- Function: create_customer(text, text, text, text)

-- DROP FUNCTION create_customer(text, text, text, text);

CREATE OR REPLACE FUNCTION create_customer(IN i_firstname text, IN i_lastname text, IN i_email text, IN i_password text, OUT status integer, OUT status_text text, OUT customer_id integer)
  RETURNS record AS
$BODY$
-- ------------------------------------------------------------------------------
-- Function create_customer
--
-- Input params:
--
-- Output params:
--     status
--     status_text
-- ------------------------------------------------------------------------------
BEGIN

    SELECT 200, 'Ok' INTO status, status_text;
    --  insert into customers
    INSERT INTO customer (
            firstname
            , lastname
            , email
            , password                     
        ) VALUES (
            i_firstname
            , i_lastname
            , i_email
            , i_password            
        );
        
    customer_id = currval('pk_seq');

    RETURN;
END;
$BODY$
  LANGUAGE 'plpgsql' VOLATILE SECURITY DEFINER
  COST 100;
GRANT EXECUTE ON FUNCTION create_customer(text, text, text, text) TO postgres;

-- Function: create_order(integer, integer)

-- DROP FUNCTION create_order(integer, integer);

CREATE OR REPLACE FUNCTION create_order(IN i_key_customer integer, IN i_key_address integer, OUT status integer, OUT status_text text, OUT order_id integer)
  RETURNS record AS
$BODY$
-- ------------------------------------------------------------------------------
-- Function create_order
--
-- Input params:
--
-- Output params:
--     status
--     status_text
-- ------------------------------------------------------------------------------
BEGIN

    SELECT 200, 'Ok' INTO status, status_text;
    --  insert into orders
    INSERT INTO orders (
            key_customer
            , key_status
            , key_address
            , delivered                   
        ) VALUES (
            i_key_customer
            , 1 -- CREATED
            , i_key_address
            , false            
        );
        
    order_id = currval('pk_seq');

    RETURN;
END;
$BODY$
  LANGUAGE 'plpgsql' VOLATILE SECURITY DEFINER
  COST 100;
GRANT EXECUTE ON FUNCTION create_order(integer,integer) TO postgres;

-- Function: save_address(bigint, text, text, text, text, text, text)

-- DROP FUNCTION save_address(bigint, text, text, text, text, text, text)

CREATE OR REPLACE FUNCTION save_address(IN i_key_customer bigint, IN i_address_line1 text, IN i_address_line2 text, IN i_postcode text, IN i_country text, IN i_region text, IN i_city text, OUT status integer, OUT status_text text, OUT address_id integer)
  RETURNS record AS
$BODY$
-- ------------------------------------------------------------------------------
-- Function save_address
--
-- Input params:
--
-- Output params:
--     status
--     status_text
-- ------------------------------------------------------------------------------
BEGIN

    SELECT 200, 'Ok' INTO status, status_text;
    --  insert into address
    INSERT INTO address (
            key_customer
            , address_line1
            , address_line2
            , postcode
            , country
            , region
            , city                  
        ) VALUES (
            i_key_customer
            , i_address_line1
            , i_address_line2
            , i_postcode
            , i_country
            , i_region
            , i_city            
        );
    address_id = currval('pk_seq');

    RETURN;
END;
$BODY$
  LANGUAGE 'plpgsql' VOLATILE SECURITY DEFINER
  COST 100;
GRANT EXECUTE ON FUNCTION save_address(bigint, text, text, text, text, text, text)TO postgres;

-- Function: deliver_order(integer, text)

-- DROP FUNCTION deliver_order(integer, text);

CREATE OR REPLACE FUNCTION deliver_order(IN i_order_id integer, IN i_changed_by text,  OUT status integer, OUT status_text text)
  RETURNS record AS
$BODY$
-- ------------------------------------------------------------------------------
-- Function deliver_order
--
-- Input params:
--
-- Output params:
--     status
--     status_text
-- ------------------------------------------------------------------------------
DECLARE
    _old_status integer;
    
BEGIN
    --
    -- Retrieve id for the old order status.
    --
    SELECT key_status FROM orders WHERE id_order = i_order_id	
    INTO _old_status;

    IF _old_status <> 1 THEN
        RAISE EXCEPTION 'WEBERROR: Function deliver_order(integer, text): Cant update order #%  when trying to set order status to DELIVERED. Comment or called by: %)', i_order_id, i_changed_by;
    END IF;


    --  update order status
    UPDATE orders
    SET
        key_status = 2 -- DELIVERED
        ,delivered = true
    WHERE
        id_order = i_order_id;

    SELECT 200, 'Order status changed from ' || _old_status || ' to DELIVERED. Comment or modified by: ' || COALESCE(i_changed_by::text, '<NULL>')
    INTO status, status_text;
    RETURN;
END;
$BODY$
  LANGUAGE 'plpgsql' VOLATILE SECURITY DEFINER
  COST 100;
GRANT EXECUTE ON FUNCTION deliver_order(integer,text) TO postgres;