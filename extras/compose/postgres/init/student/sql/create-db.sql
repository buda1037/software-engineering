CREATE USER student PASSWORD 'p';

-- https://www.postgresql.org/docs/current/sql-createdatabase.html
CREATE DATABASE student;

-- https://www.postgresql.org/docs/current/role-attributes.html
-- https://www.postgresql.org/docs/current/ddl-priv.html
-- https://www.postgresql.org/docs/current/sql-grant.html
GRANT ALL ON DATABASE student TO student;

-- https://www.postgresql.org/docs/current/sql-createtablespace.html
CREATE TABLESPACE studentspace OWNER student LOCATION '/tablespace/student';
