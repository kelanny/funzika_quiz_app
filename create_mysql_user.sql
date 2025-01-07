-- Create mysql user and grant privileges

CREATE USER 'funzika'@'%' IDENTIFIED BY 'funzika_pwd';

GRANT ALL PRIVILEGES ON *.* TO 'funzika'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;