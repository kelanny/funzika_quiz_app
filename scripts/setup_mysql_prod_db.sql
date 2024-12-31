-- prepares a MySQL server for the project testing

CREATE DATABASE IF NOT EXISTS funzika_prod_db;
CREATE USER IF NOT EXISTS 'funzika_prod'@'localhost' IDENTIFIED BY 'funzika_prod_pwd';
GRANT ALL PRIVILEGES ON `funzika_prod_db`.* TO 'funzika_prod'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'funzika_prod'@'localhost';
FLUSH PRIVILEGES;
