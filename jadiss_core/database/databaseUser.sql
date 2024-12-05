CREATE USER 'jadiss_core'@'172.18.0.1' IDENTIFIED BY 'jadiss_core##';
CREATE USER 'jadiss_core'@'172.17.0.1' IDENTIFIED BY 'jadiss_core##';
CREATE USER 'jadiss_core'@'%' IDENTIFIED BY 'jadiss_core##';

GRANT ALL PRIVILEGES ON `core`.* TO 'jadiss_core'@'172.18.0.1';
GRANT ALL PRIVILEGES ON `core`.* TO 'jadiss_core'@'172.17.0.1';
GRANT ALL PRIVILEGES ON `core`.* TO 'jadiss_core'@'%';

