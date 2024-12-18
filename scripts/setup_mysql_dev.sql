-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS funzika_dev_db;
CREATE USER IF NOT EXISTS 'funzika_dev'@'localhost' IDENTIFIED BY 'funzika_dev_pwd';
GRANT ALL PRIVILEGES ON `funzika_dev_db`.* TO 'funzika_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'funzika_dev'@'localhost';
FLUSH PRIVILEGES;
