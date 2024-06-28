CREATE TABLE dim_client(
    client_id INT PRIMARY KEY,
    "name" VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    document VARCHAR NOT NULL
);

CREATE TABLE dim_address(
    address_id INT PRIMARY KEY,
    uf VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    country VARCHAR NOT NULL
);

CREATE TABLE dim_product_category(
    category_id INT PRIMARY KEY,
    "name" VARCHAR NOT NULL
);

create table dim_seller (
seller_id INT primary key,
"name" varchar not null
);

CREATE TABLE fact_order(
    dim_client_id INT NOT NULL,
    dim_address_id INT NOT NULL,
    dim_category_product_id INT NOT NULL,
    dim_seller_id INT NOT NULL,
    order_id INT NOT NULL,
    price FLOAT NOT NULL,
    payment_method VARCHAR NOT NULL,
    "status" VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (dim_client_id,dim_address_id,dim_category_product_id,dim_seller_id,order_id),
    CONSTRAINT  fk_dim_client FOREIGN KEY (dim_client_id) REFERENCES dim_client (client_id),
    CONSTRAINT  fk_dim_address FOREIGN KEY (dim_address_id) REFERENCES dim_address (address_id),
    CONSTRAINT  fk_dim_category_product FOREIGN KEY (dim_category_product_id) REFERENCES dim_product_category (category_id)
);
