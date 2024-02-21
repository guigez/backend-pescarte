-- migrate:up

CREATE TABLE uf (
    uf_name VARCHAR(255) PRIMARY KEY,
    uf VARCHAR(2) UNIQUE NOT NULL
);

-- migrate:down

DROP TABLE IF EXISTS uf;
