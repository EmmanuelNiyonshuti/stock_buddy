-- development
CREATE DATABASE IF NOT EXISTS stockbuddy_dev_db;
CREATE USER IF NOT EXISTS 'stockbuddy_dev'@'localhost' IDENTIFIED BY '^stockbuddy**';
USE stockbuddy_dev_db;
GRANT ALL PRIVILEGES ON stockbuddy_dev_db.* TO 'stockbuddy_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'stockbuddy_dev'@'localhost';
FLUSH PRIVILEGES;


-- testing
CREATE DATABASE IF NOT EXISTS stockbuddy_test_db;
CREATE USER IF NOT EXISTS 'stockbuddy_dev'@'localhost' IDENTIFIED BY 'stock123';
USE stockbuddy_test_db;
GRANT ALL PRIVILEGES ON stockbuddy_test_db.* TO 'stockbuddy_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'stockbuddy_dev'@'localhost';
FLUSH PRIVILEGES;

