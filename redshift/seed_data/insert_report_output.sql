 
INSERT INTO report_output (transaction_id, transaction_date, amount, currency, description, client_name, country)
SELECT 
    t.transaction_id, 
    t.transaction_date, 
    t.amount, 
    t.currency, 
    t.description, 
    c.client_name, 
    c.country
FROM transactions t
JOIN clients c 
ON t.client_id = c.client_id;