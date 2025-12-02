-- This is a template for setting up the database.
-- Do not run this file directly.
-- Replace 'your_password_here' with a strong password.

-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS carnet_db;

-- 2. Create the Application User
-- We use '%' to allow connections from any IP (required because WebApp and DB are on different servers)
CREATE USER IF NOT EXISTS 'carnet_user'@'%' IDENTIFIED BY 'your_password_here';

-- 3. Grant Permissions
-- Grant only the necessary privileges to the application user
GRANT SELECT, INSERT, UPDATE, DELETE ON carnet_db.* TO 'carnet_user'@'%';

-- 4. Apply Changes
FLUSH PRIVILEGES;