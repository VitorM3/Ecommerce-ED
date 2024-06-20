CREATE TABLE dim_client(
    client_id INT PRIMARY KEY,
    "name" VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    document VARCHAR NOT NULL,
);

CREATE TABLE dim_address(
    address_id INT PRIMARY KEY,
    cep VARCHAR NOT NULL,
    uf VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    country VARCHAR NOT NULL
);

CREATE TABLE dim_product_category(
    category_id INT PRIMARY KEY,
    "name" VARCHAR NOT NULL
);

CREATE TABLE fact_order(
    dim_client_id INT PRIMARY KEY,
    dim_address_id INT PRIMARY KEY,
    dim_category_product_id INT PRIMARY KEY,
    price FLOAT NOT NULL,
    payment_method VARCHAR NOT NULL,
    "status" VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_dim_client REFERENCES dim_client (client_id),
    CONSTRAINT fk_dim_address REFERENCES dim_address (address_id),
    CONSTRAINT fk_dim_category_product REFERENCES dim_product_category (category_id)
);