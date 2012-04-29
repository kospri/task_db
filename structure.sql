CREATE SEQUENCE pk_seq;

-- Customer data
CREATE TABLE customer(
    id_customer BIGINT CONSTRAINT customer_pkey PRIMARY KEY DEFAULT nextval('pk_seq'),
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL CHECK (email~E'^[\\w-]+(?:\.[\\w-]+)*@(?:[\\w-]+\\.)+[a-zA-Z]{2,7}$'),
    password TEXT NOT NULL CHECK (length(password)>7)
);

-- Customer address
CREATE TABLE address(
    id_address BIGINT CONSTRAINT address_pkey PRIMARY KEY DEFAULT nextval('pk_seq'),
    key_customer BIGINT NOT NULL CONSTRAINT address_key_customer_fkey REFERENCES customer (id_customer),
    address_line1 TEXT NOT NULL,
    address_line2 TEXT,
    postcode TEXT NOT NULL,
    country TEXT NOT NULL,
    region TEXT,
    city TEXT
);


-- Orders placed by the customer
CREATE TABLE orders(
    id_order BIGINT CONSTRAINT orders_pkey PRIMARY KEY DEFAULT nextval('pk_seq'),
    key_customer BIGINT NOT NULL CONSTRAINT orders_key_customer_fkey REFERENCES customer (id_customer),
    key_status INTEGER NOT NULL,
    key_address BIGINT NOT NULL CONSTRAINT orders_key_customer_fkey2 REFERENCES address (id_address),
    delivered boolean NOT NULL DEFAULT false -- Flag if goods were delivered
);