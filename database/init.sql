-- This is a template for setting up the database.
-- Do not run this file directly.
-- Replace 'your_password_here' with a strong password.

-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS carnet_db;

-- 2. Drop the existing user (if it exists) to ensure a clean slate
DROP USER IF EXISTS 'your_username_here'@'%';
DROP USER IF EXISTS 'your_username_here'@'localhost';

-- 3. Create the Application User
CREATE USER 'your_username_here'@'%' IDENTIFIED BY 'your_password_here';

-- 4. Grant Permissions
-- Grant only the necessary privileges to the application user
GRANT SELECT, INSERT, UPDATE, DELETE ON carnet_db.* TO 'your_username_here'@'%';

-- 5. Apply Changes
FLUSH PRIVILEGES;