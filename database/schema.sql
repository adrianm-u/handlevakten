CREATE DATABASE handlevaktenDB;
USE handlevaktenDB;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(500) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    created_at DATE NOT NULL DEFAULT (CURRENT_DATE),
    account_type VARCHAR(25) NOT NULL CHECK (account_type IN ('user' , 'admin'))
);

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    image_url VARCHAR(255),
    description TEXT,
    updated_at DATETIME
);

CREATE TABLE stores (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    store_code VARCHAR(100) NOT NULL,
    store_logo VARCHAR(255)
);

CREATE TABLE prices (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    price INT NOT NULL CHECK (price >= 0),
    FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE,
    FOREIGN KEY (store_id)
        REFERENCES stores (store_id)
        ON DELETE CASCADE
);

CREATE TABLE price_history (
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    price DECIMAL(10 , 2 ) NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (product_id , store_id , date),
    CHECK (price >= 0),
    FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE,
    FOREIGN KEY (store_id)
        REFERENCES stores (store_id)
        ON DELETE CASCADE
);

CREATE TABLE wishlist (
    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    wishlist_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE
);

CREATE TABLE wishlist_items (
    wishlist_item_id INT AUTO_INCREMENT PRIMARY KEY,
    wishlist_id INT NOT NULL,
    product_id INT NOT NULL,
    UNIQUE (wishlist_id , product_id),
    FOREIGN KEY (wishlist_id)
        REFERENCES wishlist (wishlist_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE
);

CREATE TABLE allergens (
    allergen_id INT AUTO_INCREMENT PRIMARY KEY,
    allergen_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE product_allergens (
    product_allergen_id INT AUTO_INCREMENT PRIMARY KEY,
    allergen_id INT NOT NULL,
    product_id INT NOT NULL,
    UNIQUE (product_id , allergen_id),
    FOREIGN KEY (allergen_id)
        REFERENCES allergens (allergen_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE
);