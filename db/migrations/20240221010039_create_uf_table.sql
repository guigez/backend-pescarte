-- migrate:up

CREATE TABLE uf (
    uf_name VARCHAR(255) UNIQUE NOT NULL,
    uf VARCHAR(2) PRIMARY KEY
);

-- migrate:down

DROP TABLE IF EXISTS uf;
