-- Database creation
CREATE DATABASE IF NOT EXISTS buy_py;
USE buy_py;

-- Client table
CREATE TABLE IF NOT EXISTS client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(250) NOT NULL,
    surname VARCHAR(250) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    zip_code SMALLINT NOT NULL,
    city VARCHAR(30) NOT NULL,
    country VARCHAR(30) DEFAULT 'Portugal',
    phone_number VARCHAR(15) NOT NULL,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    birthdate DATE NOT NULL,
    is_active BOOLEAN,
    CONSTRAINT chk_email CHECK (email REGEXP '[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}'),
    CONSTRAINT chk_phone CHECK (phone_number REGEXP '^[0-9]{6,}$')
);

-- Operator table
CREATE TABLE IF NOT EXISTS operator (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(250) NOT NULL,
    surname VARCHAR(250) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    birthdate DATE NOT NULL,
    is_active BOOLEAN,
    CONSTRAINT chk_email CHECK (email REGEXP '[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}')
);

-- Product table
CREATE TABLE IF NOT EXISTS product (
    id VARCHAR(10) PRIMARY KEY,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    vat DECIMAL(5,2) NOT NULL,
    vat_amount DECIMAL(10,2) NOT NULL,
    serial_number BIGINT NOT NULL UNIQUE,
    brand VARCHAR(20) NOT NULL,
    model VARCHAR(20) NOT NULL,
    spec_tec TEXT,
    type VARCHAR(10),
    CONSTRAINT chk_price CHECK (price > 0)
);

-- Book table (extends Product)
CREATE TABLE IF NOT EXISTS book (
    product_id VARCHAR(10) PRIMARY KEY,
    isbn13 VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(50) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    publisher VARCHAR(100) NOT NULL,
    publication_date DATE,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Author table
CREATE TABLE IF NOT EXISTS author (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) COMMENT "Author's literary/pseudo name, for which he is known",
    fullname VARCHAR(100) COMMENT "Author's real full name"
);

-- BookAuthor junction table
CREATE TABLE IF NOT EXISTS book_author (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(10) NOT NULL,
    author_id INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES book(product_id),
    FOREIGN KEY (author_id) REFERENCES author(id)
);

-- Order table
CREATE TABLE IF NOT EXISTS `order` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivery_method VARCHAR(10) DEFAULT 'regular',
    status VARCHAR(10) DEFAULT 'open',
    payment_card_number BIGINT NOT NULL,
    payment_card_name VARCHAR(20) NOT NULL,
    payment_card_expiration DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES client(id),
    CONSTRAINT chk_delivery_method CHECK (delivery_method IN ('regular', 'urgent')),
    CONSTRAINT chk_status CHECK (status IN ('open', 'processing', 'pending', 'closed', 'cancelled'))
);

-- Ordered_Product junction table
CREATE TABLE IF NOT EXISTS ordered_product (
    order_id INT NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES `order`(id),
    FOREIGN KEY (product_id) REFERENCES product(id),
    CONSTRAINT chk_ordered_price CHECK (price > 0)
);

-- Recommendation table
CREATE TABLE IF NOT EXISTS recommendation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reason VARCHAR(500),
    start_date DATE,
    score TINYINT,
    CONSTRAINT chk_score CHECK (score BETWEEN 1 AND 5)
);