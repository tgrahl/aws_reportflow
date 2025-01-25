 CREATE TABLE transactions (
    transaction_id INT IDENTITY(1,1) PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients(client_id),
    transaction_date TIMESTAMP NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE clients (
    client_id INT IDENTITY(1,1) PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    country VARCHAR(50),
    signup_date DATE
);

CREATE TABLE report_output (
    transaction_id INT PRIMARY KEY,
    transaction_date TIMESTAMP NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    description VARCHAR(255),
    client_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL
);