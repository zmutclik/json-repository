-- CREATE USER IF NOT EXISTS root@localhost IDENTIFIED BY 'DB_ROOTPASSWORD';
-- SET PASSWORD FOR root@localhost = PASSWORD('DB_ROOTPASSWORD');
-- GRANT ALL ON *.* TO root@localhost WITH GRANT OPTION;

CREATE USER IF NOT EXISTS root@'%' IDENTIFIED BY 'DB_ROOTPASSWORD';
SET PASSWORD FOR root@'%' = PASSWORD('DB_ROOTPASSWORD');
GRANT ALL ON *.* TO root@'%' WITH GRANT OPTION;

CREATE USER IF NOT EXISTS user_backup@localhost IDENTIFIED BY 'BACKUP_PASS';
SET PASSWORD FOR user_backup@localhost = PASSWORD('BACKUP_PASS');
GRANT SELECT, RELOAD, PROCESS, SUPER, REPLICATION CLIENT ON *.* TO user_backup@localhost WITH GRANT OPTION;

CREATE USER IF NOT EXISTS DB_APPUSER@'%' IDENTIFIED BY 'DB_APPPASS';
SET PASSWORD FOR DB_APPUSER@'%' = PASSWORD('DB_APPPASS');

CREATE DATABASE IF NOT EXISTS DB_NAME;
GRANT ALL ON DB_NAME.* TO DB_APPUSER@'%';