-- Aufruf: psql --dbname=student --username=student --file=/init/student/sql/create-schema.sql

-- https://www.postgresql.org/docs/current/ddl-schemas.html
-- https://www.postgresql.org/docs/current/ddl-schemas.html#DDL-SCHEMAS-CREATE
-- "user-private schema" (Default-Schema: public)
CREATE SCHEMA IF NOT EXISTS AUTHORIZATION student;

ALTER ROLE student SET search_path = 'student';
