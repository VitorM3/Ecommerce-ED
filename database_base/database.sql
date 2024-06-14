/*Create Table Categories*/
CREATE TABLE Categories (
    id SERIAL PRIMARY KEY,
    "name" varchar not null,
    created_at timestamp not null default now()::timestamp,
    updated_at timestamp not null default now()::timestamp,
    deleted_at timestamp
);
/*Create Table Products*/
CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    category_id INT NOT NULL,
    "name" varchar not null,
    price float not null,
    created_at timestamp not null default now()::timestamp,
    updated_at timestamp not null default now()::timestamp,
    deleted_at timestamp,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Categories (id)
);
/*Create Table Inventory*/
CREATE TABLE Inventories (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    amount INT not null,
    created_at timestamp not null default now()::timestamp,
    updated_at timestamp not null default now()::timestamp,
    deleted_at timestamp,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES Products (id)
);
/*Create Table Address*/
CREATE TABLE Addresses (
    id SERIAL PRIMARY KEY,
    city VARCHAR not null,
    uf VARCHAR not null,
    reference VARCHAR not null,
    district VARCHAR not null,
    country VARCHAR not null,
    created_at timestamp not null default now()::timestamp,
    updated_at timestamp not null default now()::timestamp,
    deleted_at timestamp
);
/*Create Table User*/
CREATE TYPE E_Users_Type AS ENUM('ADMIN','SELLER','CLIENT');
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    address_id INT NOT NULL,
    "name" varchar not null,
    document VARCHAR not null,
    email VARCHAR not null,
    "password" VARCHAR not null,
    "type" E_Users_Type not null,
    created_at timestamp not null default now()::timestamp,
    updated_at timestamp not null default now()::timestamp,
    deleted_at timestamp,
    CONSTRAINT fk_address FOREIGN KEY (address_id) REFERENCES Addresses (id)   
);
/*Create table Order*/
CREATE TYPE E_Orders_Payment_Method AS ENUM('PIX','BANK_SLIP','CREDIT','DEBIT');
CREATE TYPE E_Orders_Status AS ENUM('PAYING','PAYED','CANCELED','OPEN','DENIED','SEPARATING','SENDED','DELIVERED','FINISHED','RETURNED');
CREATE TABLE Orders (
    id SERIAL PRIMARY KEY,
    client_id INT NOT NULL,
    delivery_address_id INT NOT NULL,
    billing_address_id INT,
    price FLOAT NOT NULL,
    payment_method E_Orders_Payment_Method NOT NULL,
    "status" E_Orders_Status NOT NULL,
    created_at timestamp not null default now()::timestamp,
    updated_at timestamp not null default now()::timestamp,
    deleted_at timestamp, 
    CONSTRAINT fk_client FOREIGN KEY (client_id) REFERENCES Users (id),
    CONSTRAINT fk_delivery_address FOREIGN KEY (delivery_address_id) REFERENCES Addresses (id),
    CONSTRAINT fk_billing_address FOREIGN KEY (billing_address_id) REFERENCES Addresses (id) 
);
/*Create Table Order_Product*/
CREATE TABLE Order_Products(
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    amount INT NOT NULL,
    created_at timestamp not null default now()::timestamp,
    updated_at timestamp not null default now()::timestamp,
    deleted_at timestamp,
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES Orders (id),
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES Products (id)
);
