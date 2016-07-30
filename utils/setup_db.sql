CREATE DATABASE dzj_characters;
CREATE USER dzj WITH PASSWORD 'dzjsql';
ALTER ROLE dzj SET client_encoding TO 'utf8';
ALTER ROLE dzj SET default_transaction_isolation TO 'read committed';
ALTER ROLE dzj SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE dzj_characters TO dzj;
\q
