-- prepares a MySQL server for the project testing

CREATE DATABASE IF NOT EXISTS funzika_test_db;
CREATE USER IF NOT EXISTS 'funzika_test'@'localhost' IDENTIFIED BY 'funzika_test_pwd';
GRANT ALL PRIVILEGES ON `funzika_test_db`.* TO 'funzika_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'funzika_test'@'localhost';
FLUSH PRIVILEGES;
