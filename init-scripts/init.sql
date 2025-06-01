-- Create a new user
CREATE USER postgres WITH PASSWORD 'postgres';

-- Create a new database
CREATE DATABASE healf_db;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE healf_db TO postgres;